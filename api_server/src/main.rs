use example::link_service_server::{LinkService, LinkServiceServer,};
use example::{LinkInfoMessage, EmptyMessage, LinkInfoMessageList};
use rusqlite::{Connection, Result};
use std::sync::{Arc, Mutex};
use tonic::{transport::Server, Request, Response, Status};

pub mod example {
    tonic::include_proto!("links");
}

#[derive(Debug)]
pub struct MyLinkService {
    db: Arc<Mutex<Connection>>,
}

#[tonic::async_trait]
impl LinkService for MyLinkService {
    async fn send_data(
        &self,
        request: Request<LinkInfoMessage>,
    ) -> Result<Response<EmptyMessage>, Status> {
        let req = request.into_inner();
        println!(
            "Received request: Link is from: {}, To: {}",
            req.from, req.to
        );
        let conn = self.db.lock().unwrap();
        conn.execute(
            "INSERT OR REPLACE INTO connections (\"from\", \"to\", latency, throughput, timestamp) VALUES (?1, ?2, ?3, ?4, strftime('%s', 'now'))",
            rusqlite::params![req.from, req.to, req.latency, req.throughput],
        ).map_err(|e| Status::internal(format!("Database error: {}", e)))?;

        Ok(Response::new(EmptyMessage{}))
    }
    async fn get_all_links(
        &self,
        _request: Request<EmptyMessage>,
    ) -> Result<Response<LinkInfoMessageList>, Status> {
        let conn = self.db.lock().unwrap();

        let mut stmt = conn
            .prepare("SELECT \"from\", \"to\", latency, throughput FROM connections")
            .map_err(|e| Status::internal(format!("DB Error: {}", e)))?;

        let links_iter = stmt
            .query_map([], |row| {
                Ok(LinkInfoMessage {
                    from: row.get(0)?,
                    to: row.get(1)?,
                    latency: row.get(2)?,
                    throughput: row.get(3)?,
                })
            })
            .map_err(|e| Status::internal(format!("Query Error: {}", e)))?;

        let links = links_iter
            .filter_map(|res| res.ok()) // Ignore failed rows
            .collect();

        let response = LinkInfoMessageList { links };

        Ok(Response::new(response))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let conn = Connection::open("database.db")?;
    conn.execute(
        "CREATE TABLE IF NOT EXISTS connections (
            \"from\" TEXT NOT NULL,
            \"to\" TEXT NOT NULL,
            latency INTEGER,
            throughput INTEGER,
            timestamp INTEGER,
            PRIMARY KEY (\"from\", \"to\")
        )",
        [],
    )?;

    let addr = "0.0.0.0:50051".parse()?;
    let db: Arc<Mutex<Connection>> = Arc::new(Mutex::new(conn));

    // Create the service
    let example_service = MyLinkService { db };

    // Start the gRPC server
    println!("Server listening on {}", addr);
    Server::builder()
        .add_service(LinkServiceServer::new(example_service))
        .serve(addr)
        .await?;

    Ok(())
}
