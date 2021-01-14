# The proper, mathematical way to calculate the inverse of the calibrations.
# Too slow and not worth the accuracy benefits (which are tiny). We'll use
# a linear approximation of the calibration curves.

from sympy import symbols, Eq, solveset
from datetime import datetime
now = datetime.now

x, y = symbols('x y')
cal = Eq(y, -0.3899 + 3.8493*x + 0.0137*x**2 - 0.0015*x**3 + 0.0002*x**4)
inv = solveset(cal,x)

Y = 24.4829 #random value in range 0 to ~40

t0 = now()
ans = [a for a in inv.subs(y,Y) if a.is_real and 0 <= a <= 10][0]
t1 = now()

print(ans, t1.microsecond - t0.microsecond)