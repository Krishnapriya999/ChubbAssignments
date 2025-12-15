 dataset$OrderDate <- as.Date(dataset$OrderDate)
library(dplyr)
monthlySales <- dataset %>%
  mutate(Month = format(OrderDate, "%Y-%m")) %>%
  group_by(Month) %>%
  summarise(TotalSales = sum(SalesAmount))
library(ggplot2)
ggplot(monthlySales, aes(x = Month, y = TotalSales, group=1)) +
  geom_line(color="blue", size=1) +
  geom_point(color="red", size=2) +
  labs(title="Monthly Sales Trend", x="Month", y="Total Sales") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))