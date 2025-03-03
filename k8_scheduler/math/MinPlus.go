package math

func Multiply(f_1, f_2 LinearFunction) LinearFunction {
	f_t := LinearFunction{0, 0, 0}
	f_t.M = f_1.M + f_2.M
	f_t.C = f_1.M * f_1.A + f_2.M * f_2.A + f_1.C + f_2.C
	return  f_t
}

func Devide(f_1, f_2 LinearFunction) LinearFunction {
	f_t := LinearFunction{0, 0, 0}
	f_t.M = f_1.M - f_2.M
	f_t.C = f_1.M * f_1.A + f_1.C - f_2.M * f_2.A - f_2.C
	return  f_t
}