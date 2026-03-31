initial_conditions = [
    0 0.5 1;
    0.01 0.5 1;
    1 1 1;
    2 2 2
];

tspan = [0 100];
trajectories = cell(size(initial_conditions,1),1);

for i = 1:size(initial_conditions,1)
    [t, sol] = solve_butterfly(initial_conditions(i,:), tspan);

    trajectories{i} = struct( ...
        't', t, ...
        'x', sol(:,1), ...
        'y', sol(:,2), ...
        'z', sol(:,3), ...
        'sol', sol);
end

plot_butterflies(trajectories);
compare_butterflies(@euclidean_metric, trajectories, tspan);