# DATOS COMPLETOS
aux <- as.data.frame(read.csv("Tesis_Obj_Zs_270923_20_11.csv"))

# 168 DEMAND POINTS
aux168 <- as.data.frame(aux[1:25, 3:5])
matrix168 <- matrix(nrow=5, ncol=5)
colnames(matrix168) <- c("10", "50", "100", "150", "200")
rownames(matrix168) <- c("16", "30", "50", "70", "100")
count = 1
for (s in 1:5){
  for (l in 1:5){
    matrix168[s,l] = aux168[count,3]
    count = count + 1
  }
}
pdf("168_runtime_20_11.pdf")
barplot(matrix168, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time", 
        main="Run time in seconds for 160 demand points \n considering 20 BLS and 11 ALS ambulances")
legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
               fill = 1:5, title = "Sites")
dev.off() 

# 270 DEMAND POINTS
aux270 <- as.data.frame(aux[26:50, 3:5])
matrix270 <- matrix(nrow=5, ncol=5)
colnames(matrix270) <- c("10", "50", "100", "150", "200")
rownames(matrix270) <- c("16", "30", "50", "70", "100")
count = 1
for (s in 1:5){
  for (l in 1:5){
    matrix270[s,l] = aux270[count,3]
    count = count + 1
  }
}
pdf("270_runtime_20_11.pdf")
barplot(matrix270, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
        main="Run time in seconds for 270 demand points \n considering 20 BLS and 11 ALS ambulances")
legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
            fill = 1:5, title = "Sites")
dev.off() 

# 500 DEMAND POINTS
aux500 <- as.data.frame(aux[51:75, 3:5])
matrix500 <- matrix(nrow=5, ncol=5)
colnames(matrix500) <- c("10", "50", "100", "150", "200")
rownames(matrix500) <- c("16", "30", "50", "70", "100")
count = 1
for (s in 1:5){
  for (l in 1:5){
    matrix500[s,l] = aux500[count,3]
    count = count + 1
  }
}
pdf("500_runtime_20_11.pdf")
barplot(matrix500, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
        main="Run time in seconds for 500 demand points \n considering 20 BLS and 11 ALS ambulances")
legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
            fill = 1:5, title = "Sites")
dev.off() 

# 900 DEMAND POINTS
aux900 <- as.data.frame(aux[76:100, 3:5])
matrix900 <- matrix(nrow=5, ncol=5)
colnames(matrix900) <- c("10", "50", "100", "150", "200")
rownames(matrix900) <- c("16", "30", "50", "70", "100")
count = 1
for (s in 1:5){
  for (l in 1:5){
    matrix900[s,l] = aux900[count,3]
    count = count + 1
  }
}
pdf("900_runtime_20_11.pdf")
barplot(matrix900, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
        main="Run time in seconds for 900 demand points \n considering 20 BLS and 11 ALS ambulances")
legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
            fill = 1:5, title = "Sites")
dev.off() 

# 1500 DEMAND POINTS
aux1500 <- as.data.frame(aux[101:125, 3:5])
matrix1500 <- matrix(nrow=5, ncol=5)
colnames(matrix1500) <- c("10", "50", "100", "150", "200")
rownames(matrix1500) <- c("16", "30", "50", "70", "100")
count = 1
for (s in 1:5){
  for (l in 1:5){
    matrix1500[s,l] = aux1500[count,3]
    count = count + 1
  }
}
pdf("1500_runtime_20_11.pdf")
barplot(matrix1500, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
        main="Run time in seconds for 1500 demand points \n considering 20 BLS and 11 ALS ambulances")
legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
            fill = 1:5, title = "Sites")
dev.off() 