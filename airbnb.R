library(plyr)

#Set directory
getwd()
setwd("/Users/cornelisvletter/desktop/progs/kaggle/airbnb")

#Load in data
sessions <- read.csv("~/Desktop/progs/kaggle/airbnb/sessions.csv")
countries <- read.csv("~/Desktop/progs/kaggle/airbnb/countries.csv")
demographic <- read.csv("~/Desktop/progs/kaggle/airbnb/age_gender_bkts.csv")
test_users <- read.csv("~/Desktop/progs/kaggle/airbnb/test_users.csv")
train_users <- read.csv("~/Desktop/progs/kaggle/airbnb/train_users_2.csv")

#Simple test

features <-  train_users[ ,-c(1,16)]
target <- train_users[, c(16)]

countriesList <- c('US', 'FR', 'CA', 'GB', 'ES', 'IT', 'PT', 'NL','DE', 'AU', 'NDF')

for (i in 1:(countriesList)){
  currenctCountry = countriesList[i]
  for (j in 1:)
}

#Transform sessions

counts <- ddply(sessions, .(sessions$user_id, df$action), nrow)
names(counts) <- c("y", "m", "Freq")
