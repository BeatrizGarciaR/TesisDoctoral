# datos COMPLETOS
#amb <- rbind(c(10, 6), c(20, 11), c(35,20))
amb <- rbind(c(35,20))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)


############# HACER GRAFICA DE BEST OBJ DE M2M1 CON BEST BOUND DE SCENARIOS


# objective value graphics demand point vs scenarios
counti = 0
#for (i in len_I){
pdf(paste("Objective_ObjZs_M2M1-Scenarios_280224_",len_L[1],'_',eta[1],'_',eta[2],".pdf", sep=""), width = 10)
par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
  
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
  
  aux_1 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
  
  aux_bb <- as.data.frame(aux_1[filas, c(2,4,6)])
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
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound)+30),
         cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound)+30),
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
  legend(x="top", legend = len_S, horiz=TRUE, cex = 2.1,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Scenarios", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  legend(x = "left",         # Posición
         legend = c("best objective M2M1", "best objective M1"), # Textos de la leyenda
         lty = c(1, 2),          # Tipo de líneas
         col = c(1, 1),          # Colores de las líneas
         lwd = 2, bty = "n", cex = 2.2)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# objective value graphics scenarios vs demand point
counti = 0
#for (i in len_I){
pdf(paste("Objective_ObjZs_M2M1-Scenarios_280224_",len_L[1],'_',eta[1],'_',eta[2],"_1.pdf", sep=""), width = 10)
par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
  
  aux <- as.data.frame(aux_0[filas, c(2,4,6)])
  matrix_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
  colnames(matrix_1) <- len_I
  rownames(matrix_1) <- len_S
  count = 1
  for (s in 1:length(len_I)){
    for (l in 1:length(len_S)){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux[count,3]) == FALSE){
        matrix_1[l,s] = aux[count,3]
      }
      else{
        matrix_1[l,s] = 0
      }
      count = count + 1
    }
  }
  
  aux_1 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
  
  aux_bb <- as.data.frame(aux_1[filas, c(2,4,6)])
  matrix_bestbound_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
  colnames(matrix_bestbound_1) <- len_I
  rownames(matrix_bestbound_1) <- len_S
  count = 1
  for (s in 1:length(len_I)){
    for (l in 1:length(len_S)){
      #matrix[s,l] = aux[count,3]
      if (is.na(aux_bb[count,3]) == FALSE){
        matrix_bestbound_1[l,s] = aux_bb[count,3]
      }
      else{
        matrix_bestbound_1[l,s] = 0
      }
      count = count + 1
    }
  }
  
  if(a == 1){
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound_1)+30),
         cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_bestbound_1)+30),
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
  legend(x="top", legend = len_I, horiz=TRUE, cex = 2.1,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Demand points", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  legend(x = "left",         # Posición
         legend = c("best objective M2M1", "best objective M1"), # Textos de la leyenda
         lty = c(1, 2),          # Tipo de líneas
         col = c(1, 1),          # Colores de las líneas
         lwd = 2, bty = "n", cex = 2.2)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# # time value graphics
# counti = 0
# #for (i in len_I){
# pdf(paste("TimeVal_ObjZs_M2M1_280224_",len_L[1],'_',eta[1],'_',eta[2],".pdf", sep=""), width = 10)
# par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
#   aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   aux <- as.data.frame(aux_0[filas, c(2,4,10)])
#   matrix <- matrix(nrow=length(len_I), ncol=length(len_S))
#   colnames(matrix) <- len_S
#   rownames(matrix) <- len_I
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
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
#   #pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
#          cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="runtime in seconds",
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
#          cex.lab=2.7, cex.axis = 2.5,xlab="demand points", xaxt = "n",
#          ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:length(len_I), labels=len_I, cex.axis = 2.5, tck = 0.02)
#   # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 15000),
#   #      xlab="demand points", ylab="runtime in seconds", xaxt = "n",
#   #      main=paste("Runtime for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   # axis(1, at=1:5, labels=len_I)
#   lines(matrix[1:length(len_I)], lwd=3, col=1)
#   points(matrix[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
#   lines(matrix[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2)
#   points(matrix[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
#   lines(matrix[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3)
#   points(matrix[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
#   lines(matrix[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4)
#   points(matrix[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
#   lines(matrix[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6)
#   legend(x="top", legend = len_S, horiz=TRUE,
#          fill = c(1, 2, 3, 4, 6), title = "Scenarios",bty = "n", cex = 2.3)
#   #dev.off()
#   counti = counti+1
# }
# dev.off()
# #}
# 
# 
# 
# # time value graphics
# counti = 0
# #for (i in len_I){
# pdf(paste("TimeVal_ObjZs_M2M1_280224_",len_L[1],'_',eta[1],'_',eta[2],"_1.pdf", sep=""), width = 10)
# par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
#   aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   aux <- as.data.frame(aux_0[filas, c(2,4,10)])
#   matrix_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
#   colnames(matrix_1) <- len_I
#   rownames(matrix_1) <- len_S
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux[count,3]) == FALSE){
#         matrix_1[l,s] = aux[count,3]
#       }
#       else{
#         matrix_1[l,s] = 0
#       }
#       count = count + 1
#     }
#   }
#   
#   #pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
#          cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="runtime in seconds",
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,4000),
#          cex.lab=2.7, cex.axis = 2.5,xlab="scenarios", xaxt = "n",
#          ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:length(len_S), labels=len_S, cex.axis = 2.5, tck = 0.02)
#   # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(0, 15000),
#   #      xlab="demand points", ylab="runtime in seconds", xaxt = "n",
#   #      main=paste("Runtime for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   # axis(1, at=1:5, labels=len_I)
#   lines(matrix_1[1:length(len_S)], lwd=3, col=1)
#   points(matrix_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
#   lines(matrix_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2)
#   points(matrix_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
#   lines(matrix_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3)
#   points(matrix_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
#   lines(matrix_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4)
#   points(matrix_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
#   lines(matrix_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6)
#   legend(x="top", legend = len_I, horiz=TRUE,
#          fill = c(1, 2, 3, 4, 6), title = "Demand points",bty = "n", cex = 2.3)
#   #dev.off()
#   counti = counti+1
# }
# dev.off()
# #}
# 

# # objective value graphics demand point vs scenarios
# counti = 0
# #for (i in len_I){
# pdf(paste("TimeVal_ObjZs_M2M1-Scenarios_280224_",len_L[1],'_',eta[1],'_',eta[2],".pdf", sep=""), width = 10)
# par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
#   aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   
#   aux <- as.data.frame(aux_0[filas, c(2,4,6)])
#   matrix <- matrix(nrow=length(len_I), ncol=length(len_S))
#   colnames(matrix) <- len_S
#   rownames(matrix) <- len_I
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
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
#   
#   aux_1 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   
#   aux_bb <- as.data.frame(aux_1[filas, c(2,4,10)])
#   matrix_bestbound <- matrix(nrow=length(len_I), ncol=length(len_S))
#   colnames(matrix_bestbound) <- len_S
#   rownames(matrix_bestbound) <- len_I
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux_bb[count,3]) == FALSE){
#         matrix_bestbound[s,l] = aux_bb[count,3]
#       }
#       else{
#         matrix_bestbound[s,l] = 0
#       }
#       count = count + 1
#     }
#   }
#   if(a == 1){
#     plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,15000),
#          cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="runtime in seconds",
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,15000),
#          cex.lab=2.7, cex.axis = 2.5,xlab="demand points", xaxt = "n",
#          ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:length(len_I), labels=len_I, cex.axis = 2.5, tck = 0.02)
#   # #pdf(paste("Objval_",eta[1],"_",eta[2],".pdf", sep=""))
#   # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix_bestbound)+2),
#   #      xlab="demand points", ylab="objective value", xaxt = "n",
#   #      main=paste("Objective value for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   # axis(1, at=1:5, labels=len_I)
#   lines(matrix[1:length(len_I)], lwd=3, col=1)
#   points(matrix_bestbound[1:length(len_I)], pch=15, cex=1.5, col=1)
#   lines(matrix_bestbound[1:length(len_I)], lwd=3, col=1, lty=2)
#   points(matrix[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
#   lines(matrix[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2)
#   points(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
#   lines(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2, lty=2)
#   points(matrix[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
#   lines(matrix[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3)
#   points(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
#   lines(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3, lty=2)
#   points(matrix[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
#   lines(matrix[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4)
#   points(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
#   lines(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4, lty=2)
#   points(matrix[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
#   lines(matrix[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6)
#   points(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
#   lines(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6, lty=2)
#   legend(x="top", legend = len_S, horiz=TRUE, cex = 2.1,
#          fill = c(1, 2, 3, 4, 6, 7, 8), title = "Scenarios", bty="n")
#   #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
#   legend(x = "right",         # Posición
#          legend = c("M2M1", "M1"), # Textos de la leyenda
#          lty = c(1, 2),          # Tipo de líneas
#          col = c(1, 1),          # Colores de las líneas
#          lwd = 2, bty = "n", cex = 2.2)
#   #dev.off()
#   counti = counti+1
# }
# dev.off()
# #}
# 
# 
# # objective value graphics scenarios vs demand point
# counti = 0
# #for (i in len_I){
# pdf(paste("TimeVal_ObjZs_M2M1-Scenarios_280224_",len_L[1],'_',eta[1],'_',eta[2],"_1.pdf", sep=""), width = 10)
# par(mfrow = c(1, length(amb)/2), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
#   aux_0 <- as.data.frame(read.csv(paste('Tesis_ObjZs_M2M1_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   
#   aux <- as.data.frame(aux_0[filas, c(2,4,6)])
#   matrix_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
#   colnames(matrix_1) <- len_I
#   rownames(matrix_1) <- len_S
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux[count,3]) == FALSE){
#         matrix_1[l,s] = aux[count,3]
#       }
#       else{
#         matrix_1[l,s] = 0
#       }
#       count = count + 1
#     }
#   }
#   
#   aux_1 <- as.data.frame(read.csv(paste('Tesis_ObjZs_Scenarios_280224_',len_L[1],'_',eta[1],'_',eta[2],'.csv', sep="")))
#   
#   aux_bb <- as.data.frame(aux_1[filas, c(2,4,10)])
#   matrix_bestbound_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
#   colnames(matrix_bestbound_1) <- len_I
#   rownames(matrix_bestbound_1) <- len_S
#   count = 1
#   for (s in 1:length(len_I)){
#     for (l in 1:length(len_S)){
#       #matrix[s,l] = aux[count,3]
#       if (is.na(aux_bb[count,3]) == FALSE){
#         matrix_bestbound_1[l,s] = aux_bb[count,3]
#       }
#       else{
#         matrix_bestbound_1[l,s] = 0
#       }
#       count = count + 1
#     }
#   }
#   
#   if(a == 1){
#     plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,15000),
#          cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="runtime in seconds",
#          xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,15000),
#          cex.lab=2.7, cex.axis = 2.5,xlab="scenarios", xaxt = "n",
#          ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:length(len_S), labels=len_S, cex.axis = 2.5, tck = 0.02)
#   # #pdf(paste("Objval_",eta[1],"_",eta[2],".pdf", sep=""))
#   # plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2, max(matrix_bestbound)+2),
#   #      xlab="demand points", ylab="objective value", xaxt = "n",
#   #      main=paste("Objective value for 16 potential sites \n considering",eta[1],
#   #                 "BLS and",eta[2],"ALS ambulances", sep=" "))
#   # axis(1, at=1:5, labels=len_I)
#   lines(matrix_1[1:length(len_S)], lwd=3, col=1)
#   points(matrix_bestbound_1[1:length(len_S)], pch=15, cex=1.5, col=1)
#   lines(matrix_bestbound_1[1:length(len_S)], lwd=3, col=1, lty=2)
#   points(matrix_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
#   lines(matrix_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2)
#   points(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
#   lines(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2, lty=2)
#   points(matrix_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
#   lines(matrix_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3)
#   points(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
#   lines(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3, lty=2)
#   points(matrix_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
#   lines(matrix_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4)
#   points(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
#   lines(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4, lty=2)
#   points(matrix_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
#   lines(matrix_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6)
#   points(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
#   lines(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6, lty=2)
#   legend(x="top", legend = len_I, horiz=TRUE, cex = 2.1,
#          fill = c(1, 2, 3, 4, 6, 7, 8), title = "Demand points", bty="n")
#   #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
#   legend(x = "right",         # Posición
#          legend = c("M2M1", "M1"), # Textos de la leyenda
#          lty = c(1, 2),          # Tipo de líneas
#          col = c(1, 1),          # Colores de las líneas
#          lwd = 2, bty = "n", cex = 2.2)
#   #dev.off()
#   counti = counti+1
# }
# dev.off()
# #}
