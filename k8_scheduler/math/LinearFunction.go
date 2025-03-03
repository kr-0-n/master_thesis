package math 

import (
	"strconv"
)

// LinearFunction represents a linear function of the form m(x + a) + c
type LinearFunction struct {
	M, C, A float64
}

// Call evaluates the function at a given x
func (lf *LinearFunction) Call(x float64) float64 {
	return lf.M*(x+lf.A) + lf.C
}

// String returns the string representation of the function
func (lf *LinearFunction) String() string {
	return strconv.FormatFloat(lf.M, 'f', -1, 64) + "(x + " +
		strconv.FormatFloat(lf.A, 'f', -1, 64) + ") + " +
		strconv.FormatFloat(lf.C, 'f', -1, 64)
}