use tonic::{transport::Server, Request, Response, Status};
use example::link_service_server::{LinkService, LinkServiceServer};
use example::{LinkInfoMessage};

pub mod example {
    tonic::include_proto!("links"); 
}

#[derive(Debug, Default)]
pub struct MyLinkService;

#[tonic::async_trait]
impl LinkService for MyLinkService {
    async fn send_data(
        &self,
        request: Request<LinkInfoMessage>,
    ) -> Result<Response<LinkInfoMessage>, Status> {
        let req = request.into_inner();
        println!("Received request: Link is from: {}, To: {}", req.from, req.to);

        // Process the request and send a response
        let response = LinkInfoMessage {
            from: req.from,
            to: req.to,
            throughput: req.throughput,
            latency: req.latency
        };

        Ok(Response::new(response))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Define the address for the server
    let addr = "127.0.0.1:50051".parse()?;

    // Create the service
    let example_service = MyLinkService::default();

    // Start the gRPC server
    println!("Server listening on {}", addr);
    Server::builder()
        .add_service(LinkServiceServer::new(example_service))
        .serve(addr)
        .await?;

    Ok(())
}