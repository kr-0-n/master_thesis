package math_test

import (
	"testing"
	"k8_scheduler/math" // Import the actual package
)

func TestLinearFunction(t *testing.T) {
	lf := math.LinearFunction{M: 2, C: 3, A: 4}

	result := lf.Call(5) // 2(5 + 4) + 3 = 21
	expected := 21.0

	if result != expected {
		t.Errorf("Expected %f, got %f", expected, result)
	}
}