function [t, sol] = solve_butterfly(x0, tspan)
    sigma = 10;
    r = 28;
    b = 8/3;

    eq = @(t, v) [
        sigma * (v(2) - v(1));
        -v(1)*v(3) + r*v(1) - v(2);
        v(1)*v(2) - b*v(3)
    ];

    [t, sol] = ode45(eq, tspan, x0);
end