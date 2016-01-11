#install.packages("e1071")
#install.packages("rpart")

library(plyr)
library(e1071)
library(rpart)

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

X <-  train_users[ ,-c(1,16)]
X$gender <- ifelse(X$gender == 'MALE', 1, ifelse(X$gender == "FEMALE", 0, NA))
target <- train_users[, c(16)]


countriesList <- c('US', 'FR', 'CA', 'GB', 'ES', 'IT', 'PT', 'NL','DE', 'AU', 'NDF', 'other')

for (i in 1:(countriesList)){
  y = ifelse(target == countriesList[i], 1, 0)
  testSet =  data.frame(y, X)
  fit <- rpart(y ~ X, method="class")
  
  
}

#Transform sessions

counts <- ddply(sessions, .(sessions$user_id, df$action), nrow)
names(counts) <- c("y", "m", "Freq")
