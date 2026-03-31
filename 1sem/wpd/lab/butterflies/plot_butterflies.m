function plot_butterflies(trajectories)
    figure;
    hold on;
    grid on;

    colors = nebula(length(trajectories));

    for i = 1:length(trajectories)
        sol = trajectories{i}.sol;

        plot3(sol(:,1), sol(:,2), sol(:,3), 'Color', colors(i,:), 'LineWidth', 1.2);
    end

    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Trajektorie');
    view(45,20);
end