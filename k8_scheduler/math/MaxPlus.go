package math

func Min(f_1, f_2 LinearFunction) LinearFunction {
	f_t := LinearFunction{0, 0, 0}
	if f_1.M < f_2.M {
		f_t.M = f_1.M
	} else {
		f_t.M = f_2.M
	}
	if f_1.C < f_2.C {
		f_t.C = f_1.C
	} else {
		f_t.C = f_2.C
	}
	f_t.A = f_1.A + f_2.A
	return  f_t
}