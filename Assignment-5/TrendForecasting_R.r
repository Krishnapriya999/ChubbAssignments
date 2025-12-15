library(dplyr)
categorySales <- dataset %>%
  group_by(Category) %>%
  summarise(TotalSales = sum(SalesAmount))
library(ggplot2)
ggplot(categorySales, aes(x=Category, y=TotalSales, fill=Category)) +
  geom_bar(stat="identity") +
  labs(title="Total Sales by Category", x="Category", y="Sales Amount") +
  theme_minimal() +
  theme(legend.position = "none")