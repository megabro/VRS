clear
clf

global m_dry y0 tspan
m_dry = 22;

y0 = [0 0];
tspan = [0 35];

optimal_ts = fzero(@find_ts, 6);

plot_ode(optimal_ts);
%plot_ode(3);
%m=14;
%plot_ode(3);

function plot_ode(ts)
    global m_dry y0 tspan
    
    [t,yv] = ode89(@(t,y)motionODE(t,y,ts), tspan, y0);
    apogee = max(yv(:,1));
    [max_speed, speed_index] = max(yv(:,2));
    fprintf('firing time:\t%.2f s\n', ts);
    fprintf('apogee:\t\t%.2f m\n', apogee);
    fprintf('max speed:\t%.2f m/s or mach %.2f\n\n', max_speed, max_speed/343);
    
    yyaxis left
    plot(t, yv(:,1));
    ylabel('Altitude, m');
    yyaxis right
    plot(t, yv(:,2));
    ylabel('Speed, m/s');
    speed_str = sprintf('\\leftarrow max speed: Mach %.2f',max_speed/343);
    text(t(speed_index),max_speed,speed_str,'FontSize',14)

    xlabel('Time, s');
    title_str = sprintf('Altitude/speed w.r.t time for %.2f kg dry mass', m_dry);
    title(title_str);
end

function height_diff = find_ts(ts)
    global y0 tspan
    
    [~,yv] = ode89(@(t,y)motionODE(t,y,ts), tspan, y0);
    height_diff = max(yv(:,1)) - 3000;
end

function dy = motionODE(t,y,ts)
    g = 9.81;
    rho = 1.204;
    Cd = 0.64;
    global m_dry
    total_m_dot = 0.4734026605229522;

    m = m_dry + max(ts-t, 0) .* total_m_dot;

    ref_area = pi * (152e-3/2).^2;
    drag_force = -sign(y(2)) .* Cd .* rho .* y(2).^ 2 .* ref_area ./ 2;
    thrust = 1200.*myHeaviside(ts-t);
    
    dy=zeros(2,1);
    
    dy(1) = y(2);
    dy(2) = -g + thrust./m + drag_force./m;
end

function y = myHeaviside(x)
    y = x >= 0;
end