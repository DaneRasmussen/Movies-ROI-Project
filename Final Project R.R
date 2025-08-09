movies <- read.csv("Movie_ROI_Table.csv", header=TRUE)
movies$animated <- as.factor(movies$animated)
movies$sequel <- as.factor(movies$sequel)
movies$remake <- as.factor(movies$remake)
movies$genre <- as.factor(movies$genre)
movies$domestic_gross <- movies$domestic_gross / 1000000
movies$production_budget <- movies$production_budget / 1000000

movies$sup <- ifelse(movies$genre == "superhero", 1, 0)
movies$sci <- ifelse(movies$genre == "sci-fi", 1, 0)

movies$supsci <- ifelse(movies$genre == "sci-fi", "goldenrod2",
                        ifelse(movies$genre == "superhero", "green3",
                               "darkblue"))

head(movies)
names(movies)
# attach(movies)

table(movies$genre)

# max(movies[movies$production_budget])
# movies$titlemovies$title[movies$production_budget == 533200000]

# Initial Scatter plot for Production Budget and GDB
plot(movies$production_budget, movies$domestic_gross,
     main="Production Budget V Gross Domestic Box-office Earnings",
     xlab="Production Budget", ylab="Domestic Box-office Earnings",)
cor(movies$production_budget, movies$domestic_gross)

# prod V box - Animated
plot(movies$production_budget, movies$domestic_gross,
     ylab="Domestic Box Office Earnings",
     xlab="Production Budget",
     col=ifelse(movies$animated == 1, "blue2", "black"), pch=20)
# legend("topleft", legend=c("Animated", "Live-action"),
#       col=c("blue2", "black"), pch=20)
# prod V box - Sequel
table(movies$sequel)
plot(movies$production_budget, movies$domestic_gross,
     ylab="Domestic Box Office Earnings",
     xlab="Production Budget",
     col=ifelse(movies$sequel == 1, "darkorange", "black"), pch=20)
# legend("topleft", legend=c("Sequel", "Not-Sequel"),
#       col=c("darkorange", "black"), pch=20)

# prod V box - Remake
table(movies$remake)
plot(movies$production_budget, movies$domestic_gross,
     ylab="Domestic Box Office Earnings",
     xlab="Production Budget",
     col=ifelse(movies$remake == 1, "seagreen1", "black"), pch=20)
# legend("topleft", legend=c("Remake", "Not-Remake"),
#       col=c("seagreen1", "black"), pch=20)

# prod v box - genres
movies$genre_col = ifelse(movies$genre == "sci-fi", "darkblue",
                   ifelse(movies$genre == "superhero", "firebrick3", 
                   ifelse(movies$genre=="fantasy"  ,"goldenrod2",
                   ifelse(movies$genre=="action", "cyan2",
                   ifelse(movies$genre=='comedy', "darkorchid1",
                   ifelse(movies$genre=="adventure", "tan",
                   ifelse(movies$genre=="biopic", "green", 
                   ifelse(movies$genre=="romance", "maroon1", "black"))))))))
movies$genre_col
par(xpd = FALSE, mar = c(5, 4, 4, 2))
plot(movies$production_budget, movies$domestic_gross,
     ylab="Domestic Box Office Earnings",
     xlab="Production Budget",
     col=movies$genre_col, pch=20,
     cex=1)
#legend(locator(1), legend=c("sci-fi", "superhero", "fantasy", "action", "comedy", "adventure", "biopic", "romance", "other"),
#       col=c("darkblue", "firebrick", "goldenrod2", "cyan2", "darkorchid1","tan","green", "maroon1", "black" ), pch=20)

# plot against max theaters showing the movie
plot(movies$max_theaters, log(movies$domestic_gross),
     ylab="Domestic Box Office Earnings",
     xlab="Maximum number of theathers")



# box-plots for indicator variables
plot(movies$animated, movies$domestic_gross, xlab="Animated", ylab="Earnings")
plot(movies$sequel, movies$domestic_gross, xlab="Sequel", ylab="Earnings")
plot(movies$remake, movies$domestic_gross, xlab="Remake", ylab="Earnings")
plot(movies$genre, movies$domestic_gross, main="Box-plots for genres", xlab="", ylab="Earnings", las=2)
plot(movies$genre, movies$domestic_roi, xlab="genre")

# distributions of production budget and gross earnings
hist(movies$domestic_gross)
hist(movies$production_budget)

# First Model - GDB - Prod
movies.model <- lm(infl_adj_domestic_bo~production_budget + max_theaters +
                     animated + sequel + remake, data=movies)
summary(movies.model)

plot(rstandard(movies.model))
plot(movies.model$residuals)

max(movies.model$residuals)
movies$title[movies.model$residuals == max(movies.model$residuals)]

cooks <- cooks.distance(movies.model)
plot(cooks, ylab="Cooks distance")
abline(h = 4/(nrow(movies) - length(coef(movies.model))), col = "red")

leverage <- hatvalues(movies.model)
plot(leverage)

plot(rstandard(movies.model), leverage, xlab="Standardised Residuals", ylab="Phat values")

model <- lm(domestic_roi ~ production_budget + sequel + animated + remake + genre, data=movies)
summary(model)


# Up to Date Model

model <- lm(log(domestic_roi+1, base=2) ~ log(production_budget, base=2) +
              sup + sci, data=movies)
summary(model)
plot(model$fitted.values ,rstandard(model), col=movies$supsci, pch=20)

#Residual V Fitted Values
plot(model$fitted.values, model$residuals, col=movies$supsci, pch=20,
     xlab="Fitted Value", ylab="Residuals")
# text(x=model$fitted.values, y=rstandard(model), labels=movies$rank, cex=0.7)

# Leverage
leverage <- hatvalues(model)
plot(leverage, pch=NA)
text(x=movies$rank, y=leverage, labels = movies$rank, cex=0.7)

movies$title[movies$rank == 280]

#Leverage V Residuals
plot(abs(model$residuals), leverage,  pch=NA, ylab="Leverage",
     xlab="Absolute value of Residuals")
text(y=leverage, x=abs(model$residuals), labels=movies$rank, cex=0.7)


# Cooks distance
cooks <- cooks.distance(model)
plot(cooks, pch=NA, ylab= "Cooks Distance", xlab="Rank")
text(x=movies$rank, y=cooks, labels=movies$rank, cex=.7)


# DFFITTS
dfits <- dffits(model)
plot(dfits, pch=NA)
text(x = 1:300, y=dfits, labels = movies$rank)


# remove outliers and recalculate model
movies$title[movies$rank == 2]


cooks[cooks > .02]
movies <- movies[-c(1,2,3,4,7,27,33,248,280), ]
#movies = movies[movies$rank != 280, ]
#movies <- movies[movies$rank > 50, ]
head(movies)

# WLS Model
wls.model <- lm(log(domestic_roi+1, base=2) ~ log(production_budget, base=2) + sup + sci, data=movies, weights = fitted(model)^1.25)
summary(wls.model)

# Equal Variance
plot(wls.model$fitted.values ,rstandard(wls.model), col=movies$supsci, pch=20, xlab="Fitted Value", ylab="Standard Residuals")

# Linearity
plot(log(movies$production_budget, base=2), log(movies$domestic_roi+1, base=2), col=movies$supsci, pch=19, ylab="Domestic ROI", xlab="Production Budget")
abline(b=model$coefficients[2], a=model$coefficient[1], col = "darkblue")
abline(b=model$coefficients[2], a=model$coefficient[1]+model$coefficient[3], col = "green3")
abline(b=model$coefficients[2], a=model$coefficient[1]+model$coefficient[4], col = "goldenrod2")
# legend("topright", legend=c("Sci-fi", "Superhero", "Other"), col=c("goldenrod2", "green3", "darkblue"), pch=20)

# Normality of Residuals
plot(density(rstandard(wls.model)), main="Density plot for Standardized Residuals")
qqnorm(wls.model$residuals)
qqline(wls.model$residuals)


# Confidence intervals
confint(wls.model)

movies[2]

plot(log(movies$production_budget), log(movies$domestic_roi+1), xlab="production budget", ylab="ROI")



plot(log(movies$production_budget, base=2), log(movies$domestic_roi+1, base=2), col=movies$supsci, pch=19, ylab="Domestic ROI", xlab="Production Budget")
abline(b=model$coefficients[2], a=model$coefficient[1], col = "darkblue")
abline(b=model$coefficients[2], a=model$coefficient[1]+model$coefficient[3], col = "green3")
abline(b=model$coefficients[2], a=model$coefficient[1]+model$coefficient[4], col = "goldenrod2")
# legend("topright", legend=c("Sci-fi", "Superhero", "Other"), col=c("goldenrod2", "green3", "darkblue"), pch=20)

plot(rstandard(model), col=movies$supsci, pch=20)
