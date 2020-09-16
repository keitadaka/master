# server.R
 
library(shiny)

shinyServer(function(input, output){
  
  output$myplot <- renderPlot({
    
    
    z_ini=input$point1
    epsilon=input$point2
    alpha=input$point3
    beta=input$point4
    gamma=input$point5
    eta=1
    tau=input$point8
    PF=input$point6      
     
    PL=8
    PP=9
    PE=13
    
    
    
    f <- function(t, z, parms){ 
           d=(epsilon*245*sin(pi/2*(z/PF)^(8/10)))/
             (min(t/tau,1)*(PE-epsilon)+epsilon)
           dz_dt=((alpha*PL*d+beta*PE*d+gamma(PP-PL)*d)*(PF-z)/PF)
           
           list(dz_dt)
                               }
    
    f1 <- function(t, z, parms){  
                                dd=(epsilon*245*sin(pi/2*(z/PF)^(8/10)))/
                                   (min(t/tau,1)*(PE-epsilon)+epsilon)
                                
                                   list(dd)
                               }
      
    library(deSolve)
    temps <- seq(from = 0, to = input$point7, by = 0.01)
    sol0 <- ode(y = z_ini, times = temps, func = f, parms = NULL,method = rkMethod ("rk4"))
    sol1 <- ode(y = z_ini, times = temps, func = f1, parms = NULL,method = rkMethod ("rk4"))
      
    
    ########### Les Onglets ##########################################
    ##################################################################
     p <- plot(sol0,ylab="Croissance",xlab="Jour", main=input$title)
    
     output$plot <- renderPlot({
                                 plot(sol1,ylab="Croissance",xlab="Jour", main="Consomation")
                              })
    ##################################################################
    output$summary <- renderPrint({
      summary(sol0) 
                                 })
    ####################################################################
    # Generate an HTML table view of the data
      output$table <- renderTable({
      data.frame(sol0)
                                 })
    ####################################################################
      if (input$point0){
        output$plot <- renderPlot({
                                    plot(sol0,ylab="Croissance",xlab="Jour", main=input$title)
                                  })
                                    p <- plot(sol1,ylab="Croissance",xlab="Jour", main="Consomation")
                       }
   ####################################################################
    })  
})