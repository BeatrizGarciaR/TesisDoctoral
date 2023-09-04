########################
###### Instancias ######
########################


tamanos_I <- c(168, 270, 500, 900, 1500)
tamanos_L <- c(16, 30, 50, 70, 100)
tamanos_S <- c(10, 50, 100, 150, 200)
# tamanos_I <- c(168)
# tamanos_L <- c(16)
# tamanos_S <- c(10)
porcentaje_L1 = 0.65
t = 9
tmax = 25
K <- c(1, 2)
rates = c(0.3,0.4,0.5)

for (aux_rate in rates){
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
      ###### tiempo de traslado ###
      #############################
      r_li <- c()
      for (sites in 1:len_L){
        # Draw N gamma distributed values
        y_rgamma <- rgamma(N, shape = 8, rate = aux_rate)
  
        # Print values to RStudio console
        r_li <- rbind(r_li, as.integer(y_rgamma))
      }
      
      # r_li <- c()
      # for (sites in 1:len_L){
      #   # Draw N gamma distributed values
      #   #y_rgamma <- rgamma(N, shape = 14.2, rate = .85) 
      #   y_rgamma <- c()
      #   for(n in 1:N){
      #     y_gamma <- rnorm(1, 20, 6)
      #     # Print values to RStudio console
      #     y_rgamma <- cbind(y_rgamma, as.integer(y_gamma))
      #   }
      #   r_li <- rbind(r_li, y_rgamma) 
      # }
      
      for (sconj in 1:length(tamanos_S)){
        #Nombre: Instancias_Prueba_I_L_S
        
        instancename <- paste('Instances_DemandFixed_',toString(tamanos_I[iconj]),'_',
                              toString(tamanos_L[jconj]),'_', toString(tamanos_S[sconj]),
                              '_', toString(aux_rate), '_', '.txt', sep = "")
  
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
        
        # Demanda solo para una muestra 
        # Demand <- matrix(nrow=1, ncol=len_I)
        # rand = rnorm(1, mean = 0.5, sd = 0.2)
        # this <- dbinom(x = 0:len_I, size = len_I, prob = rand)
        # totalAccidentes = 0
        # for (len in 1:len_I){
        #   Demand[len] = as.integer(this[len]*500)
        #   totalAccidentes = totalAccidentes + as.integer(this[len]*500)
        # }
        # for (len in 1:len_I){
        #   if (Demand[len] == 0){
        #     Demand[len] = 1
        #   }
        # }
        
        #Demanda para vaias muestras (s muestras) de cada i
        Demand <- matrix(nrow=len_S, ncol=len_I)
        totalAccidentes = 0
        for (s in 1:len_S){
          rand = rnorm(1, mean = 0.5, sd = 0.2)
          this <- dbinom(x = 0:len_I, size = len_I, prob = rand)
          
          for (len in 1:len_I){
            if(is.na(this) == TRUE){
              Demand[s,len] = 1
              totalAccidentes = totalAccidentes + 1
            }
            else{
              Demand[s,len] = as.integer(this[len]*500)
              totalAccidentes = totalAccidentes + as.integer(this[len]*500)
            }
          }
          for (len in 1:len_I){
            if (Demand[s,len] == 0){
              Demand[s,len] = 1
            }
          }
        }
        
        
        write.table(Demand, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
        
        # ###### NORMALIZADO 
        # xs <- rexp(len_S*len_I*length(K), rate = 1)
        # S <- matrix(nrow=len_S, ncol=len_I*length(K))
        # sig <- 0
        # for (len in 1:(len_I*length(K))){
        #   rand = rnorm(1)
        #   if (rand < 1){
        #     for (s in 1:len_S){
        #       S[s, len] = 0
        #     }
        #   }
        #   else{
        #     for (s in 1:len_S){
        #       sig <- sig + 1
        #       if (xs[sig] < 1){
        #         S[s, len] = 0
        #       }
        #       else if (xs[sig] < 2){
        #         S[s, len] = 1
        #       }
        #       else{
        #         S[s, len] = 2
        #       }
        #     }
        #   }
        # }
        # 
        # 
        # ###### NO NORMALIZADO 
        # # xs <- rexp(len_S*len_I*length(K), rate = 2)
        # # #xs <- rbinom(len_S*len_I*length(K), 1, 0.5)
        # # S <- matrix(nrow=len_S, ncol=len_I*length(K))
        # # sig <- 0
        # # for (s in 1:len_S){
        # #   rand = rnorm(1)
        # #   if (rand < 1){
        # #     for (len in 1:(len_I*length(K))){
        # #       S[s, len] = 0
        # #     }
        # #   }
        # #   else{
        # #     for (len in 1:(len_I*length(K))){
        # #       #x <- rexp(1, rate = 2)
        # #       #if (len < len_I*length(K)/3 || len > len_I*length(K) - len_I*length(K)/3){
        # #       randi = rnorm(1)
        # #       if (randi < 0.8){
        # #         S[s, len] = 0
        # #       }
        # #       else{
        # #         sig = sig + 1
        # #         x = xs[sig]
        # #         # if (x == 0){
        # #         #   S[s, len] = 1
        # #         # }
        # #         # else{
        # #         #   S[s, len] = 2
        # #         # }
        # #         if (x < 0.5){
        # #           S[s, len] = 0
        # #         }
        # #         else if (x < 2){
        # #           S[s, len] = 1
        # #         }
        # #         else{
        # #           S[s, len] = 2
        # #         }
        # #       }
        # # 
        # #     }
        # #   }
        # # }
        # 
        # # S <- c()
        # # for (s in 1:len_S){
        # #   S <- rbind(S, rbinom(len_I*length(K), 2, 0.1))
        # # }
        # write.table(S, file = instancename, row.names = FALSE, col.names = FALSE, append=TRUE)
        # 
        
        ################################
        ########## SCENARIOS ###########
        ################################
        
        #S <- matrix(nrow=len_S, ncol=len_I*length(K))
        proporcion_i <- c()
        sumatotal = 0
        for (i in 1:len_I){
          Demand_i = sum(Demand[,i])
          proporcion_i <- cbind(proporcion_i, Demand_i/totalAccidentes)
          sumatotal = sumatotal + Demand_i/totalAccidentes
        }
        
        S <- matrix(nrow=len_S, ncol=len_I*length(K))
        for (s in 1:len_S){
          count = 1
          for (i in 1:len_I){
            Demand_i = sample(Demand[,i], 1)
            aux <- sample(1:Demand_i, 1, prob=rexp(1:Demand_i, proporcion_i[i]))
            S[s,count] = as.integer((2*aux)/3)
            count = count + 1
            S[s,count] = as.integer(aux/3)
            count = count + 1
          }
        }
        
        #S <- sample(Demand, size=length(Demand), replace=TRUE, prob=proporcion_i)
        
        # S <- matrix(nrow=len_S, ncol=len_I*length(K))
        # for (s in 1:len_S){
        #   len = 0
        #   for (i in 1:len_I){
        #     totalaccidentes = sample(Demand[i], 1)
        #     rand = rnorm(1)
        #     if (rand < 0){
        #       rand = rand*(-1)
        #     }
        #     if (rand > 1){
        #       rand = 1
        #     }
        #     if (rand < 0.7){
        #       accidentes1 = as.numeric(as.integer(totalaccidentes*(rand)))
        #       len = len + 1
        #       S[s, len] = accidentes1
        #       len = len + 1
        #       S[s, len] = as.numeric(as.integer((totalaccidentes-accidentes1)*(rand)))
        #       
        #     }
        #     else{
        #       accidentes1 = totalaccidentes*(1-rand)
        #       len = len + 1
        #       S[s, len] = as.numeric(as.integer(accidentes1))
        #       len = len + 1
        #       S[s, len] = as.numeric(as.integer((totalaccidentes-accidentes1)*(1-rand)))
        #       
        #     }
        #   }
        # }
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
}    
