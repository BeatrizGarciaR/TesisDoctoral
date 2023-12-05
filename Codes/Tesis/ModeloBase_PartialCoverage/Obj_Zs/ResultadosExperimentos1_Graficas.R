# datos COMPLETOS
#amb <- rbind(c(10, 6), c(20, 11), c(35,20))
amb <- rbind(c(10,6), c(20,11), c(35,20))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168)
len_L <- c(16)
len_S <- c(10)

# # run time graphics
# counti = 0
# for (i in len_I){
#   filas = c(seq(from=(1+counti*25), to=((1+counti*25)+25)))
#   for (a in 1:length(amb[,1])){
#     eta <- amb[a,]
#     aux_0 <- as.data.frame(read.csv(paste('Tesis_untitled2_111123_',eta[1],'_',eta[2],'.csv', sep="")))
#     aux <- as.data.frame(aux_0[filas, 3:5])
#     matrix <- matrix(nrow=5, ncol=5)
#     colnames(matrix) <- len_S
#     rownames(matrix) <- len_L
#     count = 1
#     for (s in 1:5){
#       for (l in 1:5){
#         matrix[s,l] = aux[count,3]
#         count = count + 1
#       }
#     }
#     png(paste(i,"_runtime_",eta[1],"_",eta[2],".png", sep=""))
#     barplot(matrix, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time")
#             #main=paste("Run time in seconds for", i, "demand points \n considering",eta[1],
#                         #"BLS and",eta[2],"ALS ambulances", sep=" "))
#     legend(x="topleft", legend = len_L,
#            fill = 1:5, title = "Sites", cex=1)
#     dev.off()
#   }
#   counti = counti+1
# }


# # objective value graphics
# counti = 0
# #for (i in len_I){
# 
#   for (a in 1:length(amb[,1])){
#     # run time
#     eta <- amb[a,]
#     filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
#     aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_161123_AllAmb.csv', sep="")))
#     aux <- as.data.frame(aux_0[filas, c(3,4,6)])
#     matrix <- matrix(nrow=5, ncol=5)
#     colnames(matrix) <- len_S
#     rownames(matrix) <- len_I
#     count = 1
#     for (s in 1:5){
#       for (l in 1:5){
#         #matrix[s,l] = aux[count,3]
#         if (is.na(aux[count,3]) == FALSE){
#           matrix[s,l] = aux[count,3]
#         }
#         else{
#           matrix[s,l] = 0
#         }
#         count = count + 1
#       }
#     }
#     pdf(paste("Objval_",eta[1],"_",eta[2],".pdf", sep=""))
#     plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix)+2),
#          xlab="demand points", ylab="objective value", xaxt = "n",
#          main=paste("Objective value for 16 potential sites \n considering",eta[1],
#                     "BLS and",eta[2],"ALS ambulances", sep=" "))
#     axis(1, at=1:5, labels=len_I)
#     lines(matrix[1:5], lwd=3, col=1)
#     points(matrix[6:10], pch=16, cex=1.5, col=2)
#     lines(matrix[6:10], lwd=3, col=2)
#     points(matrix[11:15], pch=17, cex=1.5, col=3)
#     lines(matrix[11:15], lwd=3, col=3)
#     points(matrix[16:20], pch=18, cex=1.5, col=4)
#     lines(matrix[16:20], lwd=3, col=4)
#     points(matrix[21:25], pch=19, cex=1.5, col=6)
#     lines(matrix[21:25], lwd=3, col=6)
#     legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
#     dev.off()
#     counti = counti+1
#   }
# #}
# 
# 
# # gap value graphics
# counti = 0
# #for (i in len_I){
# 
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
#   #aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_161123_AllAmb.csv', sep="")))
#   aux <- as.data.frame(aux_0[filas, c(3,4,8)])
#   matrix <- matrix(nrow=5, ncol=5)
#   colnames(matrix) <- len_S
#   rownames(matrix) <- len_I
#   count = 1
#   for (s in 1:5){
#     for (l in 1:5){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux[count,3]) == FALSE){
#         matrix[s,l] = aux[count,3]
#       }
#       else{
#         matrix[s,l] = 0
#       }
#       count = count + 1
#     }
#   }
#   pdf(paste("Gapval_",eta[1],"_",eta[2],".pdf", sep=""))
#   plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix)+2),
#        xlab="demand points", ylab="objective value", xaxt = "n",
#        main=paste("Gap for 16 potential sites \n considering",eta[1],
#                   "BLS and",eta[2],"ALS ambulances", sep=" "))
#   axis(1, at=1:5, labels=len_I)
#   lines(matrix[1:5], lwd=3, col=1)
#   points(matrix[6:10], pch=16, cex=1.5, col=2)
#   lines(matrix[6:10], lwd=3, col=2)
#   points(matrix[11:15], pch=17, cex=1.5, col=3)
#   lines(matrix[11:15], lwd=3, col=3)
#   points(matrix[16:20], pch=18, cex=1.5, col=4)
#   lines(matrix[16:20], lwd=3, col=4)
#   points(matrix[21:25], pch=19, cex=1.5, col=6)
#   lines(matrix[21:25], lwd=3, col=6)
#   legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
#   dev.off()
#   counti = counti+1
# }
# #}
# 
# 
# # time value graphics
# counti = 0
# #for (i in len_I){
# 
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
#   #aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_161123_AllAmb.csv', sep="")))
#   aux <- as.data.frame(aux_0[filas, c(3,4,10)])
#   matrix <- matrix(nrow=5, ncol=5)
#   colnames(matrix) <- len_S
#   rownames(matrix) <- len_I
#   count = 1
#   for (s in 1:5){
#     for (l in 1:5){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux[count,3]) == FALSE){
#         matrix[s,l] = aux[count,3]
#       }
#       else{
#         matrix[s,l] = 0
#       }
#       count = count + 1
#     }
#   }
#   pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
#   plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 15000),
#        xlab="demand points", ylab="objective value", xaxt = "n",
#        main=paste("Runtime for 16 potential sites \n considering",eta[1],
#                   "BLS and",eta[2],"ALS ambulances", sep=" "))
#   axis(1, at=1:5, labels=len_I)
#   lines(matrix[1:5], lwd=3, col=1)
#   points(matrix[6:10], pch=16, cex=1.5, col=2)
#   lines(matrix[6:10], lwd=3, col=2)
#   points(matrix[11:15], pch=17, cex=1.5, col=3)
#   lines(matrix[11:15], lwd=3, col=3)
#   points(matrix[16:20], pch=18, cex=1.5, col=4)
#   lines(matrix[16:20], lwd=3, col=4)
#   points(matrix[21:25], pch=19, cex=1.5, col=6)
#   lines(matrix[21:25], lwd=3, col=6)
#   legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
#   dev.off()
#   counti = counti+1
# }
# #}

# # coverage graphics
accidents_covered_total <- data.frame()
for (a in 1:length(amb[,1])){
  eta <- amb[a,]
  accidents_covered <- data.frame()
  for (i in 1:length(len_I)){
    for (l in 1:length(len_L)){
      for (s in 1: length(len_S)){
        accidents <- suppressWarnings(as.data.frame(read.table(paste('Accidents_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))))
        print(paste('Accidents_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))
        datos <- c()
        datos <- cbind(datos, len_I[i], len_L[l], len_S[s])

        full <- as.data.frame(read.table(paste('Full_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
        full_expected <- matrix(ncol=len_S[s], nrow=1)
        for (scenario in 1:len_S[s]){
          total_full = 0
          for (j in 1:length(full[,1])){
            if (full[j,2] == scenario && full[j,4] == 1){
              total_full = total_full + 1
            }
          }
          full_expected_s = total_full/as.integer(accidents[scenario])
          #print(full_expected_s)
          full_expected[1, scenario] = full_expected_s
        }
        datos <- cbind(datos, prom_full_expected = mean(full_expected)*100)


        partial1 <- as.data.frame(read.table(paste('Partial1_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
        partial1_expected <- matrix(ncol=len_S[s], nrow=1)
        for (scenario in 1:len_S[s]){
          total_partial1 = 0
          for (j in 1:length(partial1[,1])){
            if (partial1[j,2] == scenario && partial1[j,4] == 1){
              total_partial1 = total_partial1 + 1
            }
          }
          partial1_expected_s = total_partial1/as.integer(accidents[scenario])
          #print(partial1_expected_s)
          partial1_expected[1, scenario] = partial1_expected_s
        }
        datos <- cbind(datos, prom_partial1_expected = mean(partial1_expected)*100)


        partial2 <- as.data.frame(read.table(paste('Partial2_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
        partial2_expected <- matrix(ncol=len_S[s], nrow=1)
        for (scenario in 1:len_S[s]){
          total_partial2 = 0
          for (j in 1:length(partial2[,1])){
            if (partial2[j,2] == scenario && partial2[j,4] == 1){
              total_partial2 = total_partial2 + 1
            }
          }
          partial2_expected_s = total_partial2/as.integer(accidents[scenario])
          #print(partial2_expected_s)
          partial2_expected[1, scenario] = partial2_expected_s
        }
        datos <- cbind(datos, prom_partial2_expected = mean(partial2_expected)*100)


        partial3 <- as.data.frame(read.table(paste('Partial3_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
        partial3_expected <- matrix(ncol=len_S[s], nrow=1)
        for (scenario in 1:len_S[s]){
          total_partial3 = 0
          for (j in 1:length(partial3[,1])){
            if (partial3[j,2] == scenario && partial3[j,4] == 1){
              total_partial3 = total_partial3 + 1
            }
          }
          partial3_expected_s = total_partial3/as.integer(accidents[scenario])
          #print(partial3_expected_s)
          partial3_expected[1, scenario] = partial3_expected_s
        }
        datos <- cbind(datos, prom_partial3_expected = mean(partial3_expected)*100)


        null <- as.data.frame(read.table(paste('Null_ObjZs_Scenarios_161123_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
        null_expected <- matrix(ncol=len_S[s], nrow=1)
        for (scenario in 1:len_S[s]){
          total_null = 0
          for (j in 1:length(null[,1])){
            if (null[j,2] == scenario && null[j,4] == 1){
              total_null = total_null + 1
            }
          }
          null_expected_s = total_null/as.integer(accidents[scenario])
          #print(null_expected_s)
          null_expected[1, scenario] = null_expected_s
        }
        datos <- cbind(datos, prom_null_expected = mean(null_expected)*100)
        accidents_covered <- rbind(accidents_covered, datos)
      }
    }
  }
  colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
  write.csv(accidents_covered, file = paste('ExpectedCoverage_ObjZs_Scenarios_161123_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
  aux <- cbind(accidents_covered, eta[1], eta[2])
  colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
  accidents_covered_total <- rbind(accidents_covered_total, aux)
}
write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_ObjZs_Scenarios_161123_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")

# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   pdf(paste("Coverage_",eta[1],"_",eta[2],".pdf", sep=""))
#   plot(as.integer(accidents_covered_total[a*5-4, 4:8]), pch=15, col=1, cex=1.5,
#        ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt = "n",
#        main=paste("Coverage percentage for 16 potential sites \n considering",eta[1],                   
#                   "BLS and",eta[2],"ALS ambulances", sep=" "))
#   axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"))
#   lines(as.integer(accidents_covered_total[a*5-4, 4:8]), lwd=3, col=1)
#   points(as.integer(accidents_covered_total[a*5-3, 4:8]), pch=16, cex=1.5, col=2)
#   lines(as.integer(accidents_covered_total[a*5-3, 4:8]), lwd=3, col=2)
#   points(as.integer(accidents_covered_total[a*5-2, 4:8]), pch=17, cex=1.5, col=3)
#   lines(as.integer(accidents_covered_total[a*5-2, 4:8]), lwd=3, col=3)
#   points(as.integer(accidents_covered_total[a*5-1, 4:8]), pch=18, cex=1.5, col=4)
#   lines(as.integer(accidents_covered_total[a*5-1, 4:8]), lwd=3, col=4)
#   points(as.integer(accidents_covered_total[a*5, 4:8]), pch=19, cex=1.5, col=6)
#   lines(as.integer(accidents_covered_total[a*5, 4:8]), lwd=3, col=6)
#   #legend(x="topright", legend = len_I, cex=0.65, fill = c(1, 2, 3, 4, 6),
#   #       title = "Demand points", bty="n")
#   dev.off()
# }


# # accidents general
# accidents_prom <- data.frame()
# for (i in 1:length(len_I)){
#   for (l in 1:length(len_L)){
#     for (s in 1: length(len_S)){
#       accidents <- suppressWarnings(as.data.frame(read.table(paste('Accidents_untitled2_111123_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))))
#       print(paste('Accidents_untitled2_111123_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))
#       cant_accidents = sum(accidents)/len_S[s]
#       porcentaje_10_6 = 16/cant_accidents
#       porcentaje_20_11 = 31/cant_accidents
#       porcentaje_35_20 = 55/cant_accidents
#       accidents_prom <- rbind(accidents_prom, c(len_I[i], len_L[l], len_S[s], cant_accidents, porcentaje_10_6, porcentaje_20_11, porcentaje_35_20))
#     }
#   }
# }
# colnames(accidents_prom) <- c("I", "L", "S", "Total Accidents Mean", "% 10 BLS & 6 ALS", "% 20 BLS & 11 ALS", "% 35 BLS & 20 ALS")
# write.csv(accidents_prom, file = paste('AccidensMean_untitled2_111123.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# #boxplot(t(full_expected))


#accidents BLS and ALS
# poner aqu?? la proporci??n de accidentes por tipo
















# # DATOS COMPLETOS
# aux <- as.data.frame(read.csv("Tesis_untitled2_111123_20_11.csv"))
# 
# # 168 DEMAND POINTS
# aux168 <- as.data.frame(aux[1:25, 3:5])
# matrix168 <- matrix(nrow=5, ncol=5)
# colnames(matrix168) <- c("10", "50", "100", "150", "200")
# rownames(matrix168) <- c("16", "30", "50", "70", "100")
# count = 1
# for (s in 1:5){
#   for (l in 1:5){
#     matrix168[s,l] = aux168[count,3]
#     count = count + 1
#   }
# }
# pdf("168_runtime_20_11.pdf")
# barplot(matrix168, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time", 
#         main="Run time in seconds for 160 demand points \n considering 20 BLS and 11 ALS ambulances")
# legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
#                fill = 1:5, title = "Sites")
# dev.off() 
# 
# # 270 DEMAND POINTS
# aux270 <- as.data.frame(aux[26:50, 3:5])
# matrix270 <- matrix(nrow=5, ncol=5)
# colnames(matrix270) <- c("10", "50", "100", "150", "200")
# rownames(matrix270) <- c("16", "30", "50", "70", "100")
# count = 1
# for (s in 1:5){
#   for (l in 1:5){
#     matrix270[s,l] = aux270[count,3]
#     count = count + 1
#   }
# }
# pdf("270_runtime_20_11.pdf")
# barplot(matrix270, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
#         main="Run time in seconds for 270 demand points \n considering 20 BLS and 11 ALS ambulances")
# legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
#             fill = 1:5, title = "Sites")
# dev.off() 
# 
# # 500 DEMAND POINTS
# aux500 <- as.data.frame(aux[51:75, 3:5])
# matrix500 <- matrix(nrow=5, ncol=5)
# colnames(matrix500) <- c("10", "50", "100", "150", "200")
# rownames(matrix500) <- c("16", "30", "50", "70", "100")
# count = 1
# for (s in 1:5){
#   for (l in 1:5){
#     matrix500[s,l] = aux500[count,3]
#     count = count + 1
#   }
# }
# pdf("500_runtime_20_11.pdf")
# barplot(matrix500, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
#         main="Run time in seconds for 500 demand points \n considering 20 BLS and 11 ALS ambulances")
# legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
#             fill = 1:5, title = "Sites")
# dev.off() 
# 
# # 900 DEMAND POINTS
# aux900 <- as.data.frame(aux[76:100, 3:5])
# matrix900 <- matrix(nrow=5, ncol=5)
# colnames(matrix900) <- c("10", "50", "100", "150", "200")
# rownames(matrix900) <- c("16", "30", "50", "70", "100")
# count = 1
# for (s in 1:5){
#   for (l in 1:5){
#     matrix900[s,l] = aux900[count,3]
#     count = count + 1
#   }
# }
# pdf("900_runtime_20_11.pdf")
# barplot(matrix900, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
#         main="Run time in seconds for 900 demand points \n considering 20 BLS and 11 ALS ambulances")
# legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
#             fill = 1:5, title = "Sites")
# dev.off() 
# 
# # 1500 DEMAND POINTS
# aux1500 <- as.data.frame(aux[101:125, 3:5])
# matrix1500 <- matrix(nrow=5, ncol=5)
# colnames(matrix1500) <- c("10", "50", "100", "150", "200")
# rownames(matrix1500) <- c("16", "30", "50", "70", "100")
# count = 1
# for (s in 1:5){
#   for (l in 1:5){
#     matrix1500[s,l] = aux1500[count,3]
#     count = count + 1
#   }
# }
# pdf("1500_runtime_20_11.pdf")
# barplot(matrix1500, beside=TRUE, col = 1:5, xlab="scenarios", ylab="run time",
#         main="Run time in seconds for 1500 demand points \n considering 20 BLS and 11 ALS ambulances")
# legend(x="topleft", legend = c("16", "30", "50", "70", "100"), 
#             fill = 1:5, title = "Sites")
# dev.off() 