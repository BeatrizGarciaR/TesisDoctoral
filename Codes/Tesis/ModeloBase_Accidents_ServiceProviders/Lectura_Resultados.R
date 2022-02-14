
tamanos_I <- c(20, 50, 100)
tamanos_L <- c(8, 20, 40)
tamanos_M = 2
tamanos_N = 3
tamanos_S <- c(5, 20, 50)
repeticiones <- 5

Optimal_value <- matrix(ncol=6)
Dispatches <- matrix(ncol=12)
Locations <- matrix(ncol=9)
Full_Coverage <- matrix(ncol=10)
Partial_Coverage <- matrix(ncol=10)
Null_Coverage <- matrix(ncol=10)

for (iconj in 1:length(tamanos_I)){
  for (jconj in 1: length(tamanos_L)){
    for (sconj in 1:length(tamanos_S)){
      for (rep in 1:repeticiones){
        #Tabla FObj
        name = paste("FObj", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Optimal_value <- rbind(Optimal_value, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                          header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                          sep = " "))
      
        #Tabla x's
        name = paste("Located", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Locations <- rbind(Locations, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                 header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                 sep = " "))
      
        #Tabla y's
        name = paste("Dispatched", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Dispatches <- rbind(Dispatches, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                   header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                   sep = " ") )
      
        #Tabla z's Full
        name = paste("Full", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Full_Coverage <- rbind(Full_Coverage, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                         header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                         sep = " "))
       
        #Tabla z's Partial
        name = paste("Partial", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Partial_Coverage <- rbind(Partial_Coverage, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                               header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                               sep = " "))
       
        #Tabla z's Partial1
        name = paste("Partial1", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Partial_Coverage <- rbind(Partial_Coverage, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                               header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                               sep = " "))
       
        #Tabla z's Null
        name = paste("Null", tamanos_I[iconj], tamanos_L[jconj], tamanos_M, tamanos_N, tamanos_S[sconj], rep, ".txt", sep = "_")
        Null_Coverage <- rbind(Null_Coverage, read.table(name,# Archivo de datos TXT indicado como string o ruta completa al archivo
                                                         header = FALSE,                                  # Si se muestra el encabezado (TRUE) o no (FALSE)
                                                         sep = " "))
      }
    }
  }
}

###################################
########### DISPATCHED ############
###################################

reps <- c(1,2,3,4,5)
for (i in 1:length(tamanos_I)){
  for (l in 1:length(tamanos_L)){
    for (s in 1:length(tamanos_S)){
      Dispatch <- matrix(ncol = 5)
      name2 = paste("Dispatched",tamanos_L[l],tamanos_I[i],tamanos_S[s],sep="_")
      for (r in 1:repeticiones){
        count1 = 0
        #print(r)
        for (dis in 1:length(Dispatches[,1])){
          #print(paste(Dispatches[dis,1], Dispatches[dis,2], Dispatches[dis,3], Dispatches[dis,4]))
          if (is.na(Dispatches[dis,1])==FALSE && Dispatches[dis,1]==tamanos_I[i] && Dispatches[dis,2]==tamanos_L[l] && Dispatches[dis,3]==tamanos_S[s] && (Dispatches[dis,4]==r)){
            count1 = count1 + 1
            #print("entra if")
          }
        }
        count1 = count1/tamanos_S[s]
        Dispatch <- rbind(Dispatch, cbind(tamanos_L[l], tamanos_I[i], tamanos_S[s], r, count1))
      }
      assign(name2, Dispatch)
    }
  }
}

# AMBULANCES DISPATCHED FOR 8 POTENTIAL SITES 
Data1 <- data.frame(Dispatched_8_20_5[,5], Dispatched_8_20_20[,5], Dispatched_8_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Dispatched_8_50_5[,5], Dispatched_8_50_20[,5], Dispatched_8_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Dispatched_8_100_5[,5], Dispatched_8_100_20[,5], Dispatched_8_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Ambulances Dispatched Considering 8 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of ambulances dispatched")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


# AMBULANCES DISPATCHED FOR 20 POTENTIAL SITES 
Data1 <- data.frame(Dispatched_20_20_5[,5], Dispatched_20_20_20[,5], Dispatched_20_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Dispatched_20_50_5[,5], Dispatched_20_50_20[,5], Dispatched_20_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Dispatched_20_100_5[,5], Dispatched_20_100_20[,5], Dispatched_20_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Ambulances Dispatched Considering 20 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of ambulances dispatched")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)

# AMBULANCES DISPATCHED FOR 40 POTENTIAL SITES 
Data1 <- data.frame(Dispatched_40_20_5[,5], Dispatched_40_20_20[,5], Dispatched_40_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Dispatched_40_50_5[,5], Dispatched_40_50_20[,5], Dispatched_40_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Dispatched_40_100_5[,5], Dispatched_40_100_20[,5], Dispatched_40_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Ambulances Dispatched Considering 40 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of ambulances dispatched")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


###################################
############# FULL ################
###################################
reps <- c(1,2,3,4,5)
for (i in 1:length(tamanos_I)){
  for (l in 1:length(tamanos_L)){
    for (s in 1:length(tamanos_S)){
      Full <- matrix(ncol = 5)
      name2 = paste("Full",tamanos_L[l],tamanos_I[i],tamanos_S[s],sep="_")
      for (r in 1:repeticiones){
        count1 = 0
        #print(r)
        for (dis in 1:length(Full_Coverage[,1])){
          #print(paste(Dispatches[dis,1], Dispatches[dis,2], Dispatches[dis,3], Dispatches[dis,4]))
          if (is.na(Full_Coverage[dis,1])==FALSE && Full_Coverage[dis,1]==tamanos_I[i] && Full_Coverage[dis,2]==tamanos_L[l] && Full_Coverage[dis,3]==tamanos_S[s] && (Full_Coverage[dis,4]==r)){
            count1 = count1 + 1
            #print("entra if")
          }
        }
        count1 = count1/tamanos_S[s]
        Full <- rbind(Full, cbind(tamanos_L[l], tamanos_I[i], tamanos_S[s], r, count1))
      }
      assign(name2, Full)
    }
  }
}

# AMBULANCES DISPATCHED FOR 8 POTENTIAL SITES 
Data1 <- data.frame(Full_8_20_5[,5], Full_8_20_20[,5], Full_8_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Full_8_50_5[,5], Full_8_50_20[,5], Full_8_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Full_8_100_5[,5], Full_8_100_20[,5], Full_8_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Full Covered Demand Points Considering 8 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points covered")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


# AMBULANCES DISPATCHED FOR 20 POTENTIAL SITES 
Data1 <- data.frame(Full_20_20_5[,5], Full_20_20_20[,5], Full_20_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Full_20_50_5[,5], Full_20_50_20[,5], Full_20_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Full_20_100_5[,5], Full_20_100_20[,5], Full_20_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Full Covered Demand Points Considering 20 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points covered")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)

# AMBULANCES DISPATCHED FOR 40 POTENTIAL SITES 
Data1 <- data.frame(Full_40_20_5[,5], Full_40_20_20[,5], Full_40_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Full_40_50_5[,5], Full_40_50_20[,5], Full_40_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Full_40_100_5[,5], Full_40_100_20[,5], Full_40_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Full Covered Demand Points Considering 40 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points covered")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


###################################
########### PARTIAL ###############
###################################
reps <- c(1,2,3,4,5)
for (i in 1:length(tamanos_I)){
  for (l in 1:length(tamanos_L)){
    for (s in 1:length(tamanos_S)){
      Partial_Cov <- matrix(ncol = 5)
      name2 = paste("Partial",tamanos_L[l],tamanos_I[i],tamanos_S[s],sep="_")
      for (r in 1:repeticiones){
        count1 = 0
        #print(r)
        for (dis in 1:length(Partial_Coverage[,1])){
          #print(paste(Dispatches[dis,1], Dispatches[dis,2], Dispatches[dis,3], Dispatches[dis,4]))
          if (is.na(Partial_Coverage[dis,1])==FALSE && Partial_Coverage[dis,1]==tamanos_I[i] && Partial_Coverage[dis,2]==tamanos_L[l] && Partial_Coverage[dis,3]==tamanos_S[s] && (Partial_Coverage[dis,4]==r)){
            count1 = count1 + 1
            #print("entra if")
          }
        }
        count1 = count1/tamanos_S[s]
        Partial_Cov <- rbind(Partial_Cov, cbind(tamanos_L[l], tamanos_I[i], tamanos_S[s], r, count1))
      }
      assign(name2, Partial_Cov)
    }
  }
}

# AMBULANCES DISPATCHED FOR 8 POTENTIAL SITES 
Data1 <- data.frame(Partial_8_20_5[,5], Partial_8_20_20[,5], Partial_8_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Partial_8_50_5[,5], Partial_8_50_20[,5], Partial_8_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Partial_8_100_5[,5], Partial_8_100_20[,5], Partial_8_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Partial Covered Demand Points Considering 8 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points partially covered")
legend("topright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


# AMBULANCES DISPATCHED FOR 20 POTENTIAL SITES 
Data1 <- data.frame(Partial_20_20_5[,5], Partial_20_20_20[,5], Partial_20_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Partial_20_50_5[,5], Partial_20_50_20[,5], Partial_20_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Partial_20_100_5[,5], Partial_20_100_20[,5], Partial_20_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Partial Covered Demand Points Considering 20 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points partially covered")
legend("topright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)

# AMBULANCES DISPATCHED FOR 40 POTENTIAL SITES 
Data1 <- data.frame(Partial_40_20_5[,5], Partial_40_20_20[,5], Partial_40_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Partial_40_50_5[,5], Partial_40_50_20[,5], Partial_40_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Partial_40_100_5[,5], Partial_40_100_20[,5], Partial_40_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Partial Covered Demand Points Considering 40 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points partially covered")
legend("topright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


###################################
########### NULL ##################
###################################

reps <- c(1,2,3,4,5)
for (i in 1:length(tamanos_I)){
  for (l in 1:length(tamanos_L)){
    for (s in 1:length(tamanos_S)){
      Null_Cov <- matrix(ncol = 5)
      name2 = paste("Null",tamanos_L[l],tamanos_I[i],tamanos_S[s],sep="_")
      for (r in 1:repeticiones){
        count1 = 0
        #print(r)
        for (dis in 1:length(Null_Coverage[,1])){
          #print(paste(Dispatches[dis,1], Dispatches[dis,2], Dispatches[dis,3], Dispatches[dis,4]))
          if (is.na(Null_Coverage[dis,1])==FALSE && Null_Coverage[dis,1]==tamanos_I[i] && Null_Coverage[dis,2]==tamanos_L[l] && Null_Coverage[dis,3]==tamanos_S[s] && (Null_Coverage[dis,4]==r)){
            count1 = count1 + 1
            #print("entra if")
          }
        }
        count1 = count1/tamanos_S[s]
        Null_Cov <- rbind(Null_Cov, cbind(tamanos_L[l], tamanos_I[i], tamanos_S[s], r, count1))
      }
      assign(name2, Null_Cov)
    }
  }
}

# AMBULANCES DISPATCHED FOR 8 POTENTIAL SITES 
Data1 <- data.frame(Null_8_20_5[,5], Null_8_20_20[,5], Null_8_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Null_8_50_5[,5], Null_8_50_20[,5], Null_8_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Null_8_100_5[,5], Null_8_100_20[,5], Null_8_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Null Covered Demand Points Considering 8 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points not covered")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)


# AMBULANCES DISPATCHED FOR 20 POTENTIAL SITES 
Data1 <- data.frame(Null_20_20_5[,5], Null_20_20_20[,5], Null_20_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Null_20_50_5[,5], Null_20_50_20[,5], Null_20_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Null_20_100_5[,5], Null_20_100_20[,5], Null_20_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Null Covered Demand Points Considering 20 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points not covered")
legend("bottomright", title="Number of scenarios", title.adj = 0.5, cex = 0.7, fill = cols, legend = c(5,20,50), horiz = T)

# AMBULANCES DISPATCHED FOR 40 POTENTIAL SITES 
Data1 <- data.frame(Null_40_20_5[,5], Null_40_20_20[,5], Null_40_20_50[,5])
colnames(Data1) <- c("5", "20", "50")
Data2 <- data.frame(Null_40_50_5[,5], Null_40_50_20[,5], Null_40_50_50[,5])
colnames(Data2) <- c("5", "20", "50")
Data3 <- data.frame(Null_40_100_5[,5], Null_40_100_20[,5], Null_40_100_50[,5])
colnames(Data3) <- c("5", "20", "50")

DataTotal <- c(Data1, Data2, Data3)

cols <- c("cadetblue1", "coral1", "olivedrab1")
boxplot(DataTotal, 
        col = cols,
        main = "Null Covered Demand Points Considering 40 Potential Sites",
        names = c("", "20", "", "", "50", "", "", "100", ""),
        xaxs=FALSE,
        xlab = "Total number of demand points", ylab = "Number of demand points not covered")
legend("bottomright", title="Number of scenarios",title.adj = 0.5, cex = 0.6, fill = cols, legend = c(5,20,50), horiz = T)


##############################
##### LOCATIONS ##############
##############################

reps <- c(1,2,3,4,5)
for (i in 1:length(tamanos_I)){
  for (l in 1:length(tamanos_L)){
    for (s in 1:length(tamanos_S)){
      Location <- matrix(ncol = 6)
      name2 = paste("Located",tamanos_L[l],tamanos_I[i],tamanos_S[s],sep="_")
      for (r in 1:repeticiones){
        count1 = 0
        count2 = 0
        #print(r)
        for (dis in 1:length(Null_Coverage[,1])){
          #print(paste(Dispatches[dis,1], Dispatches[dis,2], Dispatches[dis,3], Dispatches[dis,4]))
          if (is.na(Null_Coverage[dis,1])==FALSE && Null_Coverage[dis,1]==tamanos_I[i] && Null_Coverage[dis,2]==tamanos_L[l] && Null_Coverage[dis,3]==tamanos_S[s] && (Null_Coverage[dis,4]==r)){
            count1 = count1 + 1
            #print("entra if")
          }
        }
        count1 = count1/tamanos_S[s]
        Null_Cov <- rbind(Null_Cov, cbind(tamanos_L[l], tamanos_I[i], tamanos_S[s], r, count1))
      }
      assign(name2, Null_Cov)
    }
  }
}

