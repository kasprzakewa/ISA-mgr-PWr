function d = max_metric(x1, y1, z1, x2, y2, z2)
    d = max([abs(x1 - x2); abs(y1 - y2); abs(z1 - z2)]);
end