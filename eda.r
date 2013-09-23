library(ggplot2)

if (!('datasets' %in% ls())) {
  socrata <- read.csv('socrata-deduplicated.csv')
  datasets <- subset(socrata, displayType == 'table')
  datasets$createdAt <- as.Date(as.POSIXct(datasets$createdAt, origin = '1970-01-01'))
}

datasets$portal <- factor(datasets$portal,
  levels = names(sort(table(datasets$portal), decreasing = T)))

p1 <- ggplot(datasets) + aes(x = portal) + geom_bar() + coord_flip() +
  scale_y_log10('Number of datasets', breaks = 10^(0:4)) +
  scale_x_discrete('Data portal')

p2 <- ggplot(datasets) + aes(x = createdAt, y = portal) + geom_point(alpha = 0.1) +
  scale_x_date('Date') +
  scale_y_discrete('Data portal') +
  theme(panel.background = element_rect(fill='white')) +
  ggtitle('Dataset creation on Socrata data portals, over time\n(Each point is a dataset.)')
