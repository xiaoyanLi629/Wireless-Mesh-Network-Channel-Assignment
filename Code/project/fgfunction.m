a = 0:11;
b = [2, 1.125, 0.75, 0.375, 0.125, 0,0,0,0,0,0,0];
figure
scatter(a,b, 'ro','filled');
hold on
plot(a,b,'--black');
hold off
c = normpdf(a,5.5,1);
figure
scatter(a,c, 'ro','filled');
hold on
plot(a,c,'--black');