data = load('error_data.csv');
X = data(:,1); y = data(:,2);
plot(y,X,'rx','MarkerSize',3)
ylabel('Error')
xlabel('Number of iterations')
pause;
