########################
###### Instancias ######
########################

# tamanos_I <- c(20, 50, 80, 95)
# tamanos_L <- c(40, 50, 70, 85)
# tamanos_S <- c(12, 25, 30, 40)
#tamanos_I <- c(168, 270, 500, 900, 1500)
#tamanos_L <- c(16, 30, 50, 70, 100)
#tamanos_S <- c(10, 50, 100, 150, 200)
tamanos_I <- c(101)
tamanos_L <- c(16)
tamanos_S <- c(10)
porcentaje_L1 = 0.65
t = 9
tmax = 25
K <- c(1, 2)

for (iconj in 1:length(tamanos_I)){
  for (jconj in 1:length(tamanos_L)){
    len_I = tamanos_I[iconj]
    len_L = tamanos_L[jconj]
    I <- c()
    for (i in 1:len_I){
      I <- cbind(I, i)
    }
    
    L <- c()
    for (l in 1:len_L){
      L <- cbind(L, l)
    }
    
    pickL1 = as.integer(tamanos_L[jconj]*porcentaje_L1)
    L1 = sample(1:len_L, pickL1)
    
    # Specify sample size
    N <- len_I  ### Quiero i valores pero en cada potencial l
    
    #############################
    ###### tiempo de traslado ### Se va a cambiar por los de la API
    #############################
    r_li <- c()
    for (sites in 1:len_L){
      # Draw N gamma distributed values
      y_rgamma <- rgamma(N, shape = 14.2, rate = .85)
      
      # Print values to RStudio console
      r_li <- rbind(r_li, as.integer(y_rgamma))
    }
    
    for (sconj in 1:length(tamanos_S)){
      #Nombre: Instancias_Prueba_I_L_S
      
      instancename <- paste('InstanciasReales_EneroPeriodo1Diario',toString(tamanos_I[iconj]),'_',
                            toString(tamanos_L[jconj]),'_', toString(tamanos_S[sconj]),'.txt', sep = "")
      
      ################################
      ############# SETS #############
      ################################
      
      write(len_I, file = instancename)
      
      write(len_L, file = instancename, append=TRUE)
      
      len_S = tamanos_S[sconj]
      write(len_S, file = instancename, append=TRUE)
      
      
      ###############################
      ########## DEMANDA ###########
      ##############################
      
      Demand_Day <- read.csv("CoordenadasAccidentes_Periodo1Diario.csv")  
      colnames(Demand_Day) <- c(seq(0,31,1))
    
      write.table(Demand_Day, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
      
      totalAccidentes = 0
      for (i in 1:length(Demand_Day[,1])){
        for (j in 2:length(Demand_Day[1,])){
          totalAccidentes = totalAccidentes + Demand_Day[i,j]
        }
      }
      
      ################################
      ########## SCENARIOS ###########
      ################################
      
      proporcion_i <- c()
      sumatotal = 0
      for (i in 1:len_I){
        Demand_Day_i = sum(Demand_Day[i,2:length(Demand_Day[i,])])
        proporcion_i <- cbind(proporcion_i, Demand_Day_i/totalAccidentes)
        sumatotal = sumatotal + Demand_Day_i/totalAccidentes
      }
      
      S <- matrix(nrow=len_S, ncol=len_I*length(K))
      for (s in 1:len_S){
        count = 1
        for (i in 1:len_I){
          #aux <- sample(1:Demand_Day_i, 1, prob=rexp(1:Demand_Day_i, proporcion_i[i]))
          #S[s,count] = as.integer((2*aux)/3)
          #count = count + 1
          #S[s,count] = as.integer(aux/3)
          #count = count + 1
          Demand_Day_i = as.numeric(sample(Demand_Day[i,2:length(Demand_Day[i,])], 1))
          S[s,count] = Demand_Day_i
          count = count + 1
          Demand_Day_i = as.numeric(sample(Demand_Day[i,2:length(Demand_Day[i,])], 1))
          S[s,count] = Demand_Day_i
          count = count + 1
        }
      }
      
      write.table(S, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
      
      ################################
      ####### RESPONSE TIMES #########
      ################################
      
      write.table(r_li, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
      
      ################################
      ############ C_li ##############
      ################################     
      
      c_li <- c()
      for (l in 1:len_L){
        c_li_aux <- c()
        for (i in 1:len_I){
          if (r_li[l,i] <= t){
            c_li_aux <- cbind(c_li_aux, 1)
          }
          else {
            if (t < r_li[l,i] &&  r_li[l,i] < tmax){
              d_rli = 1 - ((r_li[l,i]-t)/(tmax-t))
              c_li_aux <- cbind(c_li_aux, d_rli)
            }
            else{
              c_li_aux <- cbind(c_li_aux, 0)
            }
          }
        }
        c_li <- rbind(c_li, c_li_aux)
      }
      
      write.table(c_li, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE) 
      
      cantMaxAmbulancias <- c(as.integer(runif(len_L, 1, 5)))
      write.table(cantMaxAmbulancias, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE) 
      
    }
  }
}

