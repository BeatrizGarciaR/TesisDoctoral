amb <- rbind(c(10, 6), c(20, 11), c(35,20))
#amb <- rbind(c(10,6))
# len_I <- c(168, 270, 500, 900, 1500)
# len_L <- c(16, 30, 50, 70, 100)
# len_S <- c(10, 50, 100, 150, 200)

# len_I <- c(168, 270, 500, 900, 1500, 2100, 3000)
# len_L <- c(30)
# len_S <- c(10, 50, 100, 150, 200, 500)

len_I <- c(168, 270, 500, 900, 1500)
len_L <- c(16)
len_S <- c(10, 50, 100, 150, 200)


# objective value graphics demand point vs scenarios
counti = 0
#for (i in len_I){
pdf(paste("Objective_NewModel_NewModel_060224.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_060224_35_20.csv', sep="")))
  
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
  
  # aux_bb <- as.data.frame(aux_0[filas, c(2,4,7)])
  # matrix_bestbound <- matrix(nrow=length(len_I), ncol=length(len_S))
  # colnames(matrix_bestbound) <- len_S
  # rownames(matrix_bestbound) <- len_I
  # count = 1
  # for (s in 1:length(len_I)){
  #   for (l in 1:length(len_S)){
  #     #matrix[s,l] = aux[count,3]
  #     if (is.na(aux_bb[count,3]) == FALSE){
  #       matrix_bestbound[s,l] = aux_bb[count,3]
  #     }
  #     else{
  #       matrix_bestbound[s,l] = 0
  #     }
  #     count = count + 1
  #   }
  # }
  if(a == 1){
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-20,max(matrix)+100),
         cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-20,max(matrix)+100),
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
  #points(matrix_bestbound[1:length(len_I)], pch=15, cex=1.5, col=1)
  #lines(matrix_bestbound[1:length(len_I)], lwd=3, col=1, lty=2)
  points(matrix[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
  lines(matrix[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2)
  #points(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], pch=16, cex=1.5, col=2)
  #lines(matrix_bestbound[(length(len_I)+1):(2*length(len_I))], lwd=3, col=2, lty=2)
  points(matrix[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
  lines(matrix[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3)
  #points(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], pch=17, cex=1.5, col=3)
  #lines(matrix_bestbound[(2*length(len_I)+1):(3*length(len_I))], lwd=3, col=3, lty=2)
  points(matrix[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
  lines(matrix[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4)
  #points(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], pch=18, cex=1.5, col=4)
  #lines(matrix_bestbound[(3*length(len_I)+1):(4*length(len_I))], lwd=3, col=4, lty=2)
  points(matrix[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
  lines(matrix[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6)
  #points(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], pch=19, cex=1.5, col=6)
  #lines(matrix_bestbound[(4*length(len_I)+1):(5*length(len_I))], lwd=3, col=6, lty=2)
  legend(x="top", legend = len_S, horiz=TRUE, cex = 2.3,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Scenarios", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  # legend(x = "bottomright",         # Posición
  #        legend = c("best objective", "best bound"), # Textos de la leyenda
  #        lty = c(1, 2),          # Tipo de líneas
  #        col = c(1, 1),          # Colores de las líneas
  #        lwd = 2, bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# objective value graphics scenarios vs demand point
counti = 0
#for (i in len_I){
pdf(paste("Objective_NewModel_NewModel_060224_1.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_060224_35_20.csv', sep="")))
  
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
  
  # aux_bb <- as.data.frame(aux_0[filas, c(2,4,7)])
  # matrix_bestbound_1 <- matrix(nrow=length(len_S), ncol=length(len_I))
  # colnames(matrix_bestbound_1) <- len_I
  # rownames(matrix_bestbound_1) <- len_S
  # count = 1
  # for (l in 1:length(len_S)){
  #   for (s in 1:length(len_I)){
  #     #matrix[s,l] = aux[count,3]
  #     if (is.na(aux_bb[count,3]) == FALSE){
  #       matrix_bestbound_1[s,l] = aux_bb[count,3]
  #     }
  #     else{
  #       matrix_bestbound_1[s,l] = 0
  #     }
  #     count = count + 1
  #   }
  # }
  
  if(a == 1){
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(min(matrix_1)-20,max(matrix_1)+100),
         cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="objective value",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(min(matrix_1)-20,max(matrix_1)+100),
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
  #points(matrix_bestbound_1[1:length(len_S)], pch=15, cex=1.5, col=1)
  #lines(matrix_bestbound_1[1:length(len_S)], lwd=3, col=1, lty=2)
  points(matrix_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
  lines(matrix_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2)
  #points(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], pch=16, cex=1.5, col=2)
  #lines(matrix_bestbound_1[(length(len_S)+1):(2*length(len_S))], lwd=3, col=2, lty=2)
  points(matrix_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
  lines(matrix_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3)
  #points(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], pch=17, cex=1.5, col=3)
  #lines(matrix_bestbound_1[(2*length(len_S)+1):(3*length(len_S))], lwd=3, col=3, lty=2)
  points(matrix_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
  lines(matrix_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4)
  #points(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], pch=18, cex=1.5, col=4)
  #lines(matrix_bestbound_1[(3*length(len_S)+1):(4*length(len_S))], lwd=3, col=4, lty=2)
  points(matrix_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
  lines(matrix_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6)
  #points(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], pch=19, cex=1.5, col=6)
  #lines(matrix_bestbound_1[(4*length(len_S)+1):(5*length(len_S))], lwd=3, col=6, lty=2)
  legend(x="top", legend = len_I, horiz=TRUE, cex = 2.3,
         fill = c(1, 2, 3, 4, 6, 7, 8), title = "Demand points", bty="n")
  #legend(x="topleft", legend = len_S, horiz=TRUE, cex = 0.9, fill = c(1, 2, 3, 4, 6), title = "Scenarios")
  # legend(x = "bottomright",         # Posición
  #        legend = c("best objective", "best bound"), # Textos de la leyenda
  #        lty = c(1, 2),          # Tipo de líneas
  #        col = c(1, 1),          # Colores de las líneas
  #        lwd = 2, bty = "n", cex = 2.3)
  #dev.off()
  counti = counti+1
}
dev.off()
#}


# time value graphics
counti = 0
#for (i in len_I){
pdf(paste("Timeval_NewModel_NewModel_060224.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_060224_35_20.csv', sep="")))
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
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix)+100),
         cex.lab=2.7, cex.axis = 2.5, xlab="demand points", ylab="runtime in seconds",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix[1:length(len_I)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix)+100),
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
pdf(paste("Timeval_NewModel_NewModel_060224_1.pdf", sep=""), width = 20)
par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
for (a in 1:length(amb[,1])){
  # run time
  eta <- amb[a,]
  filas = c(seq(from=(1+counti*(5*length(len_I))), to=((1+counti*(5*length(len_I)))+((5*length(len_I))-1))))
  aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_060224_35_20.csv', sep="")))
  aux <- as.data.frame(aux_0[filas, c(2,4,10)])
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
  
  #pdf(paste("Timeval_",eta[1],"_",eta[2],".pdf", sep=""))
  if(a == 1){
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_1)+100),
         cex.lab=2.7, cex.axis = 2.5, xlab="scenarios", ylab="runtime in seconds",
         xaxt= "n", tck = 0.02) #ann = FALSE,
    title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
  } else{
    plot(matrix_1[1:length(len_S)], pch=15, col=1, cex=1.5, ylim=c(0,max(matrix_1)+100),
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


# # time value graphics demand points vs scenarios
# ### CUANDO SI TIENE TODOS LOS DATOS EN LAS 3 GRAFICAS
# counti = 0
# #for (i in len_I){
# ###pdf(paste("Timeval_NewModel_NewModel_060224_",eta[1],"_",eta[2],".pdf", sep=""))
# pdf(paste("Timeval_NewModel_NewModel_060224.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   # run time
#   eta <- amb[a,]
#   filas = c(seq(from=(1+counti*25), to=((1+counti*25)+24)))
#   aux_0 <- as.data.frame(read.csv(paste('Tesis_NewModel_NewModel_060224_35_20.csv', sep="")))
#   aux <- as.data.frame(aux_0[filas, c(3,4,10)])
#   matrix <- matrix(nrow=5, ncol=5)
#   colnames(matrix) <- len_S
#   rownames(matrix) <- len_I
#   count = 1
#   for (s in 1:length(len_S)){
#     for (l in 1:length(len_I)){
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
#   if(a == 1){
#     plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2,max(matrix)+20), cex.lab=2.7, cex.axis = 2.5,
#          xlab="demand points", ylab="runtime in seconds", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix)-2,max(matrix)+20), cex.lab=2.7, cex.axis = 2.5,
#          xlab="demand points", xaxt = "n",ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:5, labels=len_I, cex.axis = 2.5, tck = 0.02)
#   lines(matrix[1:5], lwd=3, col=1)
#   points(matrix[6:10], pch=16, cex=1.5, col=2)
#   lines(matrix[6:10], lwd=3, col=2)
#   points(matrix[11:15], pch=17, cex=1.5, col=3)
#   lines(matrix[11:15], lwd=3, col=3)
#   points(matrix[16:20], pch=18, cex=1.5, col=4)
#   lines(matrix[16:20], lwd=3, col=4)
#   points(matrix[21:25], pch=19, cex=1.5, col=6)
#   lines(matrix[21:25], lwd=3, col=6)
#   points(matrix[26:30], pch=20, cex=1.5, col=7)
#   lines(matrix[26:30], lwd=3, col=7)
#   points(matrix[31:35], pch=20, cex=1.5, col=8)
#   lines(matrix[31:35], lwd=3, col=8)
#   legend(x="top", legend = len_S, horiz=TRUE, cex = 2.3,
#          fill = c(1, 2, 3, 4, 6, 7, 8), title = "Scenarios", bty="n")
#   counti = counti+1
# }
# dev.off()
# #}
# 
# 
# # time value graphics scenarios vs demand point
# ### CUANDO SI TIENE TODOS LOS DATOS EN LAS 3 GRAFICAS
# counti = 0
# #for (i in len_I){
# ###pdf(paste("Timeval_NewModel_NewModel_060224_",eta[1],"_",eta[2],".pdf", sep=""))
# pdf(paste("Timeval_NewModel_NewModel_060224_1.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   eta <- amb[a,]
#   matrix_new <- t(matrix)
#   if(a == 1){
#     plot(matrix_new[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix_new)-2,max(matrix_new)+20), cex.lab=2.7, cex.axis = 2.5,
#          xlab="scenarios", ylab="runtime in seconds", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(matrix_new[1:5], pch=15, col=1, cex=1.5, ylim=c(min(matrix_new)-2,max(matrix_new)+20), cex.lab=2.7, cex.axis = 2.5,
#          xlab="scenarios", xaxt = "n",ylab="runtime in seconds", tck = 0.02)
#     title(paste(eta[1], "BLS and",eta[2],"ALS ambulances", sep=" "), cex.main=3.5)
#   }
#   axis(1, at=1:5, labels=len_S, cex.axis = 2.5, tck = 0.02)
#   lines(matrix_new[1:5], lwd=3, col=1)
#   points(matrix_new[6:10], pch=16, cex=1.5, col=2)
#   lines(matrix_new[6:10], lwd=3, col=2)
#   points(matrix_new[11:15], pch=17, cex=1.5, col=3)
#   lines(matrix_new[11:15], lwd=3, col=3)
#   points(matrix_new[16:20], pch=18, cex=1.5, col=4)
#   lines(matrix_new[16:20], lwd=3, col=4)
#   points(matrix_new[21:25], pch=19, cex=1.5, col=6)
#   lines(matrix_new[21:25], lwd=3, col=6)
#   points(matrix_new[26:30], pch=20, cex=1.5, col=7)
#   lines(matrix_new[26:30], lwd=3, col=7)
#   points(matrix_new[31:35], pch=20, cex=1.5, col=8)
#   lines(matrix_new[31:35], lwd=3, col=8)
#   legend(x="top", legend = len_I, horiz=TRUE, cex = 2.3,
#          fill = c(1, 2, 3, 4, 6, 7, 8), title = "Demand points", bty="n")
#   counti = counti+1
# }
# dev.off()
# #}


# accidents_covered_total <- data.frame()
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   accidents_covered <- data.frame()
#   for (i in len_I){
#     for (l in len_L){
#       for (s in len_S){
# 
#         print(paste('I_Accidents_NewModel_060224_', i,'_',l,'_',s,eta[1],'_',eta[2],'.txt'))
# 
#         accident_aux <- as.data.frame(read.table(paste('I_Accidents_NewModel_NewModel_060224_', i,'_',l,'_',s,'.txt', sep="")))
#         accidents <- as.data.frame(read.table(paste('Accidents_NewModel_NewModel_060224_', i,'_',l,'_',s,'.txt', sep="")))
# 
# 
#         aux_0 <- as.data.frame(read.table(paste('OnTime_Obj_NewModel_NewModel_060224_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
#         aux_0 <- aux_0[,-2]
#         colnames(aux_0) <- c("S", "L", "K", "I", "OnTime")
# 
# 
#         aux_1 <- as.data.frame(read.table(paste('Delayed_Obj_NewModel_NewModel_060224_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
#         aux_1 <- aux_1[,-2]
#         colnames(aux_1) <- c("S", "L", "K", "I", "Delayed")
# 
# 
#         aux_2 <- as.data.frame(read.table(paste('NotAssigned_Obj_NewModel_NewModel_060224_',i,'_',l,'_',s,'_',eta[1],'_',eta[2],'.txt', sep="")))
#         aux_2 <- aux_2[,-2]
#         colnames(aux_2) <- c("S", "L", "K", "I", "NotAssigned")
# 
# 
#         full_expected <- matrix(ncol=s, nrow=1)
#         partial1_expected <- matrix(ncol=s, nrow=1)
#         partial2_expected <- matrix(ncol=s, nrow=1)
#         partial3_expected <- matrix(ncol=s, nrow=1)
#         null_expected <- matrix(ncol=s, nrow=1)
# 
#         datos <- c()
#         datos <- cbind(datos, i, l, s)
# 
#         for (s_aux in 1:s){
# 
#           demand_points <- matrix(nrow=i, ncol=4)
# 
#           if (length(aux_0) != 0){
#             on_time <- subset(aux_0, S==s_aux)
#           } else{
#             on_time <- c(0, 0, 0, 0, 0)
#             colnames(on_time) <- c("S", "L", "K", "I", "OnTime")
#           }
# 
#           if (length(aux_1) != 0){
#             delayed <- subset(aux_1, S==s_aux)
#           } else{
#             delayed <- c(0, 0, 0, 0, 0)
#             colnames(delayed) <- c("S", "L", "K", "I", "Delayed")
#           }
# 
#           if (length(aux_2) != 0){
#             notAssigned <- subset(aux_2, S==s_aux)
#           } else{
#             notAssigned <- c(0, 0, 0, 0, 0)
#             colnames(notAssigned) <- c("S", "L", "K", "I", "NotAssigned")
#           }
# 
#           for (i_aux in 1:i){
# 
#             if (accident_aux[s_aux,i_aux] != 0){
#               on_time_1 <- subset(on_time, I==i_aux)
#               if (length(on_time_1) > 0){
#                 demand_points[i_aux,1] = length(on_time_1[,1])
#               }
# 
# 
#               delayed_1 <- subset(delayed, I==i_aux)
#               if (length(delayed_1) > 0){
#                 demand_points[i_aux,2] = length(delayed_1[,1])
#               }
# 
# 
#               notAssigned_1 <- subset(notAssigned, I==i_aux)
#               if (length(notAssigned_1) > 0){
#                 demand_points[i_aux,3] = sum(notAssigned_1[,5])
#               }
# 
#             } else{
#               demand_points[i_aux,1] = 0
#               demand_points[i_aux,2] = 0
#               demand_points[i_aux,3] = 0
#             }
#             demand_points[i_aux,4] = accident_aux[s_aux,i_aux]
# 
#           }
# 
# 
#           total_full = 0
#           total_partial1 = 0
#           total_partial2 = 0
#           total_partial3 = 0
#           total_null = 0
#           for (i in 1:i){
#             #print(paste("i", i))
#             if (demand_points[i,4] != 0){
#               if (demand_points[i,3] == demand_points[i,4]){
#                 total_null = total_null + 1
#                 #print("null")
#               }
#               if (demand_points[i,1] == demand_points[i,4]){
#                 total_full = total_full + 1
#                 #print("full")
#               }
#               if (demand_points[i,2] != 0){
#                 if (demand_points[i,1] + demand_points[i,2] == demand_points[i,4]){
#                   total_partial1 = total_partial1 + 1
#                   #print("p1")
#                 }
#               }
#               if (demand_points[i,3] != 0){
#                 if(demand_points[i,1] != 0 && demand_points[i,1] + demand_points[i,3] == demand_points[i,4]){
#                   total_partial2 = total_partial2 + 1
#                   #print("p2")
#                 }
#                 if (demand_points[i,2] != 0){
#                   if(demand_points[i,1] + demand_points[i,2] + demand_points[i,3] == demand_points[i,4]){
#                     total_partial3 = total_partial3 + 1
#                     #print("p3")
#                   }
#                 }
#               }
#             }
#           }
#           full_expected_s = total_full/as.integer(accidents[s_aux])
#           full_expected[1, s_aux] = full_expected_s
#           partial1_expected_s = total_partial1/as.integer(accidents[s_aux])
#           partial1_expected[1, s_aux] = partial1_expected_s
#           partial2_expected_s = total_partial2/as.integer(accidents[s_aux])
#           partial2_expected[1, s_aux] = partial2_expected_s
#           partial3_expected_s = total_partial3/as.integer(accidents[s_aux])
#           partial3_expected[1, s_aux] = partial3_expected_s
#           null_expected_s = total_null/as.integer(accidents[s_aux])
#           null_expected[1, s_aux] = null_expected_s
# 
#         }
#         datos <- cbind(datos, prom_full_expected = mean(full_expected)*100)
#         datos <- cbind(datos, prom_partial1_expected = mean(partial1_expected)*100)
#         datos <- cbind(datos, prom_partial2_expected = mean(partial2_expected)*100)
#         datos <- cbind(datos, prom_partial3_expected = mean(partial3_expected)*100)
#         datos <- cbind(datos, prom_null_expected = mean(null_expected)*100)
#         datos <- cbind(datos, c(eta[1], eta[2]))
#         accidents_covered <- rbind(accidents_covered, datos)
#       }
#     }
#   }
#   colnames(accidents_covered) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage")
#   write.csv(accidents_covered, file = paste('ExpectedCoverage_Obj_NewModel_NewModel_060224_', eta[1],'_',eta[2],'.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
#   aux <- cbind(accidents_covered, eta[1], eta[2])
#   colnames(aux) <- c("I", "L", "S", "% Full accident coverage", "% Partial1 accident coverage", "% Partial2 accident coverage", "% Partial3 accident coverage", "% Null accident coverage", "BLS ambulances", "ALS ambulances")
#   accidents_covered_total <- rbind(accidents_covered_total, aux)
# }
# write.csv(accidents_covered_total, file = paste('ExpectedCoverageTotal_Obj_NewModel_NewModel_060224_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# 
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
#     ind_1 = ind_1 + 5
#     ind_2 = ind_2 + 5
#   }
# }
# colnames(prom_coverage) <- c("I", "L", "Amb 1", "Amb 2", "Mean % Full", "Mean % P1", "Mean % P2", "Mean % P3", "Mean % Null")
# write.csv(prom_coverage, file = paste('MeanCoverageTotal_Obj_NewModel_NewModel_060224_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# 
# # MEAN COVERAGE BY SCENARIOS
# pdf(paste("Coverage_NewModel_NewModel_060224.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   #pdf(paste("Coverage_NewModel_NewModel_060224_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(as.numeric(prom_coverage[(a*5-4), 5:9]), pch=15, col=1, cex=1.5, cex.lab=2.7, cex.axis = 2.5,
#          ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(as.numeric(prom_coverage[(a*5-4), 5:9]), pch=15, col=1, cex=1.5, cex.lab=2.7, cex.axis = 2.5,
#          ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   }
# 
#   axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"), cex.axis = 2.5, tck = 0.02)
#   lines(as.integer(prom_coverage[a*5-4, 5:9]), lwd=3, col=1)
#   points(as.integer(prom_coverage[a*5-3, 5:9]), pch=16, cex=1.5, col=2)
#   lines(as.integer(prom_coverage[a*5-3, 5:9]), lwd=3, col=2)
#   points(as.integer(prom_coverage[a*5-2, 5:9]), pch=17, cex=1.5, col=3)
#   lines(as.integer(prom_coverage[a*5-2, 5:9]), lwd=3, col=3)
#   points(as.integer(prom_coverage[a*5-1, 5:9]), pch=18, cex=1.5, col=4)
#   lines(as.integer(prom_coverage[a*5-1, 5:9]), lwd=3, col=4)
#   points(as.integer(prom_coverage[a*5, 5:9]), pch=19, cex=1.5, col=6)
#   lines(as.integer(prom_coverage[a*5, 5:9]), lwd=3, col=6)
#   legend(x="top", legend = len_I, cex=2.2, horiz=TRUE, fill = c(1, 2, 3, 4, 6),
#          title = "Demand points", bty="n")
#   #dev.off()
# }
# dev.off()
# 
# ###### IR CAMBIANDO ESTO POR LOS L ############
# ind_1 = 1
# prom_coverage_1 <- data.frame()
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   for (s in 1:length(len_S)){
#     datos <- c()
#     datos <- cbind(datos, len_S[s], len_L[1], eta[1], eta[2])
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10,ind_1+15,ind_1+20),4]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10,ind_1+15,ind_1+20),5]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10,ind_1+15,ind_1+20),6]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10,ind_1+15,ind_1+20),7]))
#     datos <- cbind(datos, mean(accidents_covered_total[c(ind_1,ind_1+5,ind_1+10,ind_1+15,ind_1+20),8]))
# 
#     prom_coverage_1 <- rbind(prom_coverage_1, datos)
# 
#     ind_1 = ind_1 + 1
#   }
# }
# colnames(prom_coverage_1) <- c("I", "L", "Amb 1", "Amb 2", "Mean % Full", "Mean % P1", "Mean % P2", "Mean % P3", "Mean % Null")
# write.csv(prom_coverage_1, file = paste('MeanCoverageTotal_Obj_NewModel_NewModel_060224_1_','.csv', sep=""), col.names=TRUE, row.names=FALSE, dec = ".")
# 
# # MEAN COVERAGE BY DEMAND POINTS
# pdf(paste("Coverage_NewModel_NewModel_060224_1.pdf", sep=""), width = 20)
# par(mfrow = c(1, 3), mar=c(4.5, 5, 3.1, 0.9))
# for (a in 1:length(amb[,1])){
#   eta = amb[a,]
#   #pdf(paste("Coverage_NewModel_NewModel_060224_",eta[1],"_",eta[2],".pdf", sep=""))
#   if(a == 1){
#     plot(as.numeric(prom_coverage_1[(a*5-4), 5:9]), pch=15, col=1, cex=1.5, cex.lab=2.7, cex.axis = 2.5,
#          ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   } else{
#     plot(as.numeric(prom_coverage_1[(a*5-4), 5:9]), pch=15, col=1, cex=1.5, cex.lab=2.7, cex.axis = 2.5,
#          ylim=c(0, 100), ylab="% accidents coverage", xlab = "Coverage type", xaxt= "n", tck = 0.02) #ann = FALSE,
#     title(paste(eta[1],"BLS and",eta[2],"ALS ambulances", sep=" "), cex.main = 3.5)
#   }
# 
#   axis(1, at=1:5, labels=c("Full", "Partial1", "Partial2", "Partial3", "Null"), cex.axis = 2.5, tck = 0.02)
#   lines(as.integer(prom_coverage_1[a*5-4, 5:9]), lwd=3, col=1)
#   points(as.integer(prom_coverage_1[a*5-3, 5:9]), pch=16, cex=1.5, col=2)
#   lines(as.integer(prom_coverage_1[a*5-3, 5:9]), lwd=3, col=2)
#   points(as.integer(prom_coverage_1[a*5-2, 5:9]), pch=17, cex=1.5, col=3)
#   lines(as.integer(prom_coverage_1[a*5-2, 5:9]), lwd=3, col=3)
#   points(as.integer(prom_coverage_1[a*5-1, 5:9]), pch=18, cex=1.5, col=4)
#   lines(as.integer(prom_coverage_1[a*5-1, 5:9]), lwd=3, col=4)
#   points(as.integer(prom_coverage_1[a*5, 5:9]), pch=19, cex=1.5, col=6)
#   lines(as.integer(prom_coverage_1[a*5, 5:9]), lwd=3, col=6)
#   legend(x="top", legend = len_S, cex=2.2, horiz=TRUE, fill = c(1, 2, 3, 4, 6),
#          title = "Scenarios", bty="n")
#   #dev.off()
# }
# dev.off()
