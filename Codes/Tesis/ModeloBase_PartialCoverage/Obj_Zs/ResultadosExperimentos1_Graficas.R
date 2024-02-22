# datos COMPLETOS
amb <- rbind(c(10, 6), c(20, 11), c(35,20))
#amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)


# objective value graphics demand point vs scenarios
counti = 0
#for (i in len_I){
pdf(paste("Objective_Obj_Zs_Scenarios_060224.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_Obj_Zs_Scenarios_060224_AllAmb.csv', sep="")))

  aux <- as.data.frame(aux_0[filas, c(2,4,6)])
  matrix <- matrix(nrow=length(len_I), ncol=length(len_S))
  colnames(matrix) <- len_S
  rownames(matrix) <- len_I
  count = 1
  for (s in 1:length(len_I)){
    for (l in 1:length(len_S)){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux[count,3]) == FALSE){
        matrix[s,l] = aux[count,3]
      }
      else{
        matrix[s,l] = 0
      }
      count = count + 1
    }
  }

  aux_bb <- as.data.frame(aux_0[filas, c(2,4,7)])
  matrix_bestbound <- matrix(nrow=length(len_I), ncol=length(len_S))
  colnames(matrix_bestbound) <- len_S
  rownames(matrix_bestbound) <- len_I
  count = 1
  for (s in 1:length(len_I)){
    for (l in 1:length(len_S)){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux_bb[count,3]) == FALSE){
        matrix_bestbound[s,l] = aux_bb[count,3]
      }
      else{
        matrix_bestbound[s,l] = 0
      }
      count = count + 1
    }
  }
  if(a == 1){
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound)+20),
         cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound)+20),
         cex.lab=2.7, cex.axis = 2.5,xlab="demand points", xaxt = "n",
         ylab="objective value", tck = 0.02)
    title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
  }
  axis(1, at=1:length(len_I), labels=len_I, cex.axis = 2.5, tck = 0.02)
  # #pdf(paste("Objval_",eta[1],"_",eta[2],".pdf", sep=""))
  # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix_bestbound)+2),
  #      xlab="demand points", ylab="objective value", xaxt = "n",
  #      main=paste("Objective value for 16 potential sites \n considering",eta[1],
  #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
  # axis(1, at=1:5, labels=len_I)
  lines(matrix[1:length(len_I)], lwd=3, col=1)
  points(matrix_bestbound[1:length(len_I)], pch=15, cex=1.5, col=1)
  lines(matrix_bestbound[1:length(len_I)], lwd=3, col=1, lty=2)
  points(matrix[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
  lines(matrix[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2)
  points(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
  lines(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2, lty=2)
  points(matrix[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
  lines(matrix[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3)
  points(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
  lines(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3, lty=2)
  points(matrix[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
  lines(matrix[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4)
  points(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
  lines(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4, lty=2)
  points(matrix[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
  lines(matrix[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6)
  points(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
  lines(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6, lty=2)
  legend(x="top", legend = len_S, horiz=TRUE, cex = 2.3,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Scenarios", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  legend(x = "left",         # Posición
         legend = c("best objective", "best bound"), # Textos de la leyenda
         lty = c(1, 2),          # Tipo de líneas
         col = c(1, 1),          # Colores de las líneas
         lwd = 2, bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# objective value graphics scenarios vs demand point
counti = 0
#for (i in len_I){
pdf(paste("Objective_Obj_Zs_Scenarios_060224_1.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  matrix_1 <- t(matrix)
  matrix_bestbound_1 <- t(matrix_bestbound)

  if(a == 1){
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound_1)+20),
         cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound_1)+20),
         cex.lab=2.7, cex.axis = 2.5,xlab="scenarios", xaxt = "n",
         ylab="objective value", tck = 0.02)
    title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
  }
  axis(1, at=1:length(len_S), labels=len_S, cex.axis = 2.5, tck = 0.02)
  # #pdf(paste("Objval_",eta[1],"_",eta[2],".pdf", sep=""))
  # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix_bestbound)+2),
  #      xlab="demand points", ylab="objective value", xaxt = "n",
  #      main=paste("Objective value for 16 potential sites \n considering",eta[1],
  #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
  # axis(1, at=1:5, labels=len_I)
  lines(matrix_1[1:length(len_S)], lwd=3, col=1)
  points(matrix_bestbound_1[1:length(len_S)], pch=15, cex=1.5, col=1)
  lines(matrix_bestbound_1[1:length(len_S)], lwd=3, col=1, lty=2)
  points(matrix_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
  lines(matrix_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2)
  points(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
  lines(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2, lty=2)
  points(matrix_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
  lines(matrix_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3)
  points(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
  lines(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3, lty=2)
  points(matrix_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
  lines(matrix_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4)
  points(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
  lines(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4, lty=2)
  points(matrix_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
  lines(matrix_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6)
  points(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
  lines(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6, lty=2)
  legend(x="top", legend = len_I, horiz=TRUE, cex = 2.3,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Demand points", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  legend(x = "left",         # Posición
         legend = c("best objective", "best bound"), # Textos de la leyenda
         lty = c(1, 2),          # Tipo de líneas
         col = c(1, 1),          # Colores de las líneas
         lwd = 2, bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# # gap value graphics
# counti = 0
# #for (i in len_I){
#
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
#   #aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_060224_AllAmb.csv', sep="")))
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



# time value graphics
counti = 0
#for (i in len_I){
pdf(paste("Timeval_Obj_Zs_Scenarios_060224.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_Obj_Zs_Scenarios_060224_AllAmb.csv', sep="")))
  aux <- as.data.frame(aux_0[filas, c(2,4,10)])
  matrix <- matrix(nrow=length(len_I), ncol=length(len_S))
  colnames(matrix) <- len_S
  rownames(matrix) <- len_I
  count = 1
  for (s in 1:length(len_I)){
    for (l in 1:length(len_S)){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux[count,3]) == FALSE){
        matrix[s,l] = aux[count,3]
      }
      else{
        matrix[s,l] = 0
      }
      count = count + 1
    }
  }
  #pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
  if(a == 1){
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
         cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="runtime in seconds",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
         cex.lab=2.7, cex.axis = 2.5,xlab="demand points", xaxt = "n",
         ylab="runtime in seconds", tck = 0.02)
    title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
  }
  axis(1, at=1:length(len_I), labels=len_I, cex.axis = 2.5, tck = 0.02)
  # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 15000),
  #      xlab="demand points", ylab="runtime in seconds", xaxt = "n",
  #      main=paste("Runtime for 16 potential sites \n considering",eta[1],
  #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
  # axis(1, at=1:5, labels=len_I)
  lines(matrix[1:length(len_I)], lwd=3, col=1)
  points(matrix[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
  lines(matrix[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2)
  points(matrix[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
  lines(matrix[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3)
  points(matrix[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
  lines(matrix[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4)
  points(matrix[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
  lines(matrix[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6)
  legend(x="top", legend = len_S, horiz=TRUE,
         fill = c(1, 2, 3, 4, 6), title = "Scenarios",bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}



# time value graphics
counti = 0
#for (i in len_I){
pdf(paste("Timeval_Obj_Zs_Scenarios_060224_1.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  matrix_1 <- t(matrix)

  #pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
  if(a == 1){
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
         cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="runtime in seconds",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
         cex.lab=2.7, cex.axis = 2.5,xlab="scenarios", xaxt = "n",
         ylab="runtime in seconds", tck = 0.02)
    title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
  }
  axis(1, at=1:length(len_S), labels=len_S, cex.axis = 2.5, tck = 0.02)
  # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 15000),
  #      xlab="demand points", ylab="runtime in seconds", xaxt = "n",
  #      main=paste("Runtime for 16 potential sites \n considering",eta[1],
  #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
  # axis(1, at=1:5, labels=len_I)
  lines(matrix_1[1:length(len_S)], lwd=3, col=1)
  points(matrix_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
  lines(matrix_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2)
  points(matrix_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
  lines(matrix_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3)
  points(matrix_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
  lines(matrix_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4)
  points(matrix_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
  lines(matrix_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6)
  legend(x="top", legend = len_I, horiz=TRUE,
         fill = c(1, 2, 3, 4, 6), title = "Demand points",bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}

# # # coverage
# accidents_covered_total <- data.frame()
# for (a in 1:length(amb[,1])){
#   eta <- amb[a,]
#   accidents_covered <- data.frame()
#   for (i in 1:length(len_I)){
#     for (l in 1:length(len_L)){
#       for (s in 1: length(len_S)){
#         accidents <- suppressWarnings(as.data.frame(read.table(paste('Accidents_ObjZs_Scenarios_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))))
#         print(paste('Accidents_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '.txt', sep=""))
#         datos <- c()
#         datos <- cbind(datos, len_I[i], len_L[l], len_S[s])
# 
#         full <- as.data.frame(read.table(paste('Full_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         full_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_full = 0
#           for (j in 1:length(full[,1])){
#             if (full[j,2] == scenario && full[j,4] == 1){
#               total_full = total_full + 1
#             }
#           }
#           full_expected_s = total_full/as.integer(accidents[scenario])
#           #print(full_expected_s)
#           full_expected[1, scenario] = full_expected_s
#         }
#         datos <- cbind(datos, prom_full_expected = mean(full_expected)*100)
# 
# 
#         partial1 <- as.data.frame(read.table(paste('Partial1_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial1_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial1 = 0
#           for (j in 1:length(partial1[,1])){
#             if (partial1[j,2] == scenario && partial1[j,4] == 1){
#               total_partial1 = total_partial1 + 1
#             }
#           }
#           partial1_expected_s = total_partial1/as.integer(accidents[scenario])
#           #print(partial1_expected_s)
#           partial1_expected[1, scenario] = partial1_expected_s
#         }
#         datos <- cbind(datos, prom_partial1_expected = mean(partial1_expected)*100)
# 
# 
#         partial2 <- as.data.frame(read.table(paste('Partial2_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial2_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial2 = 0
#           for (j in 1:length(partial2[,1])){
#             if (partial2[j,2] == scenario && partial2[j,4] == 1){
#               total_partial2 = total_partial2 + 1
#             }
#           }
#           partial2_expected_s = total_partial2/as.integer(accidents[scenario])
#           #print(partial2_expected_s)
#           partial2_expected[1, scenario] = partial2_expected_s
#         }
#         datos <- cbind(datos, prom_partial2_expected = mean(partial2_expected)*100)
# 
# 
#         partial3 <- as.data.frame(read.table(paste('Partial3_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         partial3_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_partial3 = 0
#           for (j in 1:length(partial3[,1])){
#             if (partial3[j,2] == scenario && partial3[j,4] == 1){
#               total_partial3 = total_partial3 + 1
#             }
#           }
#           partial3_expected_s = total_partial3/as.integer(accidents[scenario])
#           #print(partial3_expected_s)
#           partial3_expected[1, scenario] = partial3_expected_s
#         }
#         datos <- cbind(datos, prom_partial3_expected = mean(partial3_expected)*100)
# 
# 
#         null <- as.data.frame(read.table(paste('Null_ObjZs_Scenarios_060224_', len_I[i], '_', len_L[l], '_', len_S[s], '_',eta[1],'_',eta[2],'.txt', sep="")))
#         null_expected <- matrix(ncol=len_S[s], nrow=1)
#         for (scenario in 1:len_S[s]){
#           total_null = 0
#           for (j in 1:length(null[,1])){
#             if (null[j,2] == scenario && null[j,4] == 1){
#               total_null = total_null + 1
#             }
#           }
#           null_expected_s = total_null/as.integer(accidents[scenario])
#           #print(null_expected_s)
#           null_expected[1, scenario] = null_expected_s
#         }
#         datos <- cbind(datos, prom_null_expected = mean(null_expected)*100)
#         accidents_covered <- rbind(accidents_covered, datos)
#       }
#     }
#   }
#   colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
#   write.csv(accidents_covered, file = paste('ExpectedCoverage_ObjZs_Scenarios_060224_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
#   aux <- cbind(accidents_covered, eta[1], eta[2])
#   colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
#   accidents_covered_total <- rbind(accidents_covered_total, aux)
# }
# write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_ObjZs_Scenarios_060224_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# 
# ##### mean coverage percentage graphics scenarios
# ###### IR CAMBIANDO ESTO POR LOS L ############
# ind_1 = 1
# ind_2 = 5
# prom_coverage <- data.frame()
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   for (i in 1:length(len_I)){
#     datos <- c()
#     datos <- cbind(datos, len_I[i], len_L[1], eta[1], eta[2])
#     datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,4]))
#     datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,5]))
#     datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,6]))
#     datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,7]))
#     datos <- cbind(datos, mean(accidents_covered_total[ind_1:ind_2,8]))
# 
#     prom_coverage <- rbind(prom_coverage, datos)
# 
#     ind_1 = ind_1 + length(len_I)
#     ind_2 = ind_2 + length(len_S)
#   }
# }
# colnames(prom_coverage) <- c("I", "L", "Amb 1", "Amb 2", "Mean % Full", "Mean % P1", "Mean % P2", "Mean % P3", "Mean % Null")
# write.csv(prom_coverage, file = paste('MeanCoverageTotal_ObjZs_Scenarios_060224_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# 
# #coverage mean scenarios graphics
# pdf(paste("Coverage_Obj_Zs_Scenarios_060224.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   #pdf(paste("Coverage_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(as.numeric(prom_coverage[a*length(len_I)-((length(len_I)-1)), 5:9]), pch=15, col=1, cex=1.5, ylim=c(0,100),
#          cex.lab=2.7, cex.axis = 2.5, xlab="coverage type", ylab="% accidents coverage",
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(as.numeric(prom_coverage[a*length(len_I)-(length(len_I)-1), 5:9]), pch=15, col=1, cex=1.5, ylim=c(0,100),
#          cex.lab=2.7, cex.axis = 2.5,xlab="coverage type", xaxt = "n",
#          ylab="% accident coverage", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"), cex.axis = 2.5, tck = 0.02)
#   # plot(as.numeric(prom_coverage[a*5-4, 5:9]), pch=15, col=1, cex=1.5,
#   #      ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt = "n",
#   #      main=paste("Mean coverage percentage for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   #
#   # axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"))
#   lines(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-1), 5:9]), lwd=3, col=1)
#   points(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-2), 5:9]), pch=16, cex=1.5, col=2)
#   lines(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-2), 5:9]), lwd=3, col=2)
#   points(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-3), 5:9]), pch=17, cex=1.5, col=3)
#   lines(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-3), 5:9]), lwd=3, col=3)
#   # points(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-4), 5:9]), pch=18, cex=1.5, col=4)
#   # lines(as.integer(prom_coverage[a*length(len_I)-(length(len_I)-4), 5:9]), lwd=3, col=4)
#   # points(as.integer(prom_coverage[a*length(len_I), 5:9]), pch=19, cex=1.5, col=6)
#   # lines(as.integer(prom_coverage[a*length(len_I), 5:9]), lwd=3, col=6)
#   legend(x="top", legend = len_I, horiz=TRUE,
#          fill = c(1, 2, 3, 4, 6), title = "Demand points",bty = "n", cex = 2.2)
#   # legend(x="topleft", legend = len_I, cex=0.75, fill = c(1, 2, 3, 4, 6),
#   #        title = "Demand points", bty="n")
#   # dev.off()
# }
# dev.off()
# 
# 
# ##### mean coverage demand points percentage graphics
# ###### IR CAMBIANDO ESTO POR LOS L ############
# ind_1 = 1
# prom_coverage_1 <- data.frame()
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   for (s in 1:length(len_S)){
#     datos <- c()
#     datos <- cbind(datos, len_S[s], len_L[1], eta[1], eta[2])
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10),4]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10),5]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10),6]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10),7]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10),8]))
#     
#     prom_coverage_1 <- rbind(prom_coverage_1, datos)
#     
#     ind_1 = ind_1 + 1
#   }
# }
# colnames(prom_coverage_1) <- c("I", "L", "Amb 1", "Amb 2", "Mean % Full", "Mean % P1", "Mean % P2", "Mean % P3", "Mean % Null")
# write.csv(prom_coverage_1, file = paste('MeanCoverageTotal_ObjZs_Scenarios_060224_1_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# 
# #coverage graphics 
# pdf(paste("Coverage_Obj_Zs_Scenarios_060224_1.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   #pdf(paste("Coverage_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(as.numeric(prom_coverage_1[a*5-4, 5:9]), pch=15, col=1, cex=1.5, ylim=c(0,100),
#          cex.lab=2.7, cex.axis = 2.5, xlab="coverage type", ylab="% accidents coverage", 
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(as.numeric(prom_coverage_1[a*5-4, 5:9]), pch=15, col=1, cex=1.5, ylim=c(0,100),
#          cex.lab=2.7, cex.axis = 2.5,xlab="coverage type", xaxt = "n",
#          ylab="% accident coverage", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"), cex.axis = 2.5, tck = 0.02)
#   # plot(as.numeric(prom_coverage[a*5-4, 5:9]), pch=15, col=1, cex=1.5,
#   #      ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt = "n",
#   #      main=paste("Mean coverage percentage for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   # 
#   # axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"))
#   lines(as.integer(prom_coverage_1[a*5-4, 5:9]), lwd=3, col=1)
#   points(as.integer(prom_coverage_1[a*5-3, 5:9]), pch=16, cex=1.5, col=2)
#   lines(as.integer(prom_coverage_1[a*5-3, 5:9]), lwd=3, col=2)
#   points(as.integer(prom_coverage_1[a*5-2, 5:9]), pch=17, cex=1.5, col=3)
#   lines(as.integer(prom_coverage_1[a*5-2, 5:9]), lwd=3, col=3)
#   points(as.integer(prom_coverage_1[a*5-1, 5:9]), pch=18, cex=1.5, col=4)
#   lines(as.integer(prom_coverage_1[a*5-1, 5:9]), lwd=3, col=4)
#   points(as.integer(prom_coverage_1[a*5, 5:9]), pch=19, cex=1.5, col=6)
#   lines(as.integer(prom_coverage_1[a*5, 5:9]), lwd=3, col=6)
#   legend(x="top", legend = len_S, horiz=TRUE, 
#          fill = c(1, 2, 3, 4, 6), title = "Scenarios",bty = "n", cex = 2.2)
#   # legend(x="topleft", legend = len_I, cex=0.75, fill = c(1, 2, 3, 4, 6),
#   #        title = "Demand points", bty="n")
#   # dev.off()
# }
# dev.off()
