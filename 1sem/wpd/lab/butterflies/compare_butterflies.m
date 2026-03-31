function d = compare_butterflies(metric_func, trajectories, tspan)
    t_common = linspace(tspan(1), tspan(2), 1000);

    x1 = interp1(trajectories{1}.t, trajectories{1}.x, t_common);
    y1 = interp1(trajectories{1}.t, trajectories{1}.y, t_common);
    z1 = interp1(trajectories{1}.t, trajectories{1}.z, t_common);

    x2 = interp1(trajectories{2}.t, trajectories{2}.x, t_common);
    y2 = interp1(trajectories{2}.t, trajectories{2}.y, t_common);
    z2 = interp1(trajectories{2}.t, trajectories{2}.z, t_common);

    d = metric_func(x1, y1, z1, x2, y2, z2);

    figure;
    plot(t_common, d, 'm', 'LineWidth', 1.5);
    grid on;
    title('Odległość między trajektoriami');
    xlabel('t');
    ylabel('d(t)');
end