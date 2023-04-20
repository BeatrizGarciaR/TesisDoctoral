
## 900 DEMAND POINTS 
aux <- read.csv("ResultadosExperimentos1_900.csv")  
#a <- aux[9:81,5:7]
a <- aux[1:7, 5:19]

colnames(a) <- c("10", "50", "100", "150", "200", 
                 "10", "50", "100", "150", "200", 
                 "10", "50", "100", "150", "200")

boxplot(a, main = "900 demand points", 
        xlab = "Scenarios", vertical = TRUE, method = "jitter", 
        pch = 19, col = 1:5)

## 500 DEMAND POINTS 
aux1 <- read.csv("ResultadosExperimentos1_500.csv")  
#a <- aux[9:81,5:7]
a1 <- aux1[,1:15]

colnames(a1) <- c("10", "50", "100", "150", "200", 
                 "10", "50", "100", "150", "200", 
                 "10", "50", "100", "150", "200")

boxplot(a1, main = "500 demand points", 
        xlab = "Scenarios", vertical = TRUE, method = "jitter", 
        pch = 19, col = 1:5)


## 270 DEMAND POINTS 
aux2 <- read.csv("ResultadosExperimentos1_270.csv")  
a2 <- aux2[,1:15]

colnames(a2) <- c("10", "50", "100", "150", "200", 
                  "10", "50", "100", "150", "200", 
                  "10", "50", "100", "150", "200")

boxplot(a2, main = "270 demand points", 
        xlab = "Scenarios", vertical = TRUE, method = "jitter", 
        pch = 19, col = 1:5)


## 168 DEMAND POINTS 
aux3 <- read.csv("ResultadosExperimentos1_168.csv")  
a3 <- aux3[,1:15]

colnames(a3) <- c("10", "50", "100", "150", "200", 
                  "10", "50", "100", "150", "200", 
                  "10", "50", "100", "150", "200")

boxplot(a3, main = "168 demand points", 
        xlab = "Scenarios", vertical = TRUE, method = "jitter", 
        pch = 19, col = 1:5)


# library(ggplot2)
# 
# ggplot (datos, aes (x = equipo, y = aumentar, llenar = programa)) + 
#   geom_boxplot ()


