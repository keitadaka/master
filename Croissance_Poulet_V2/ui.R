# UI.R

shinyUI(fluidPage(
  titlePanel("Croissance du poulet"), 
  
  sidebarLayout( 
    sidebarPanel(
      textInput("title", "Changer le nom du graphe de croisssance ici", value="Croissance du poulet"),
      
      checkboxInput('point0', 'Consomation - Croissance (coher pour permuter)'),
      numericInput("point1", "Poids initiale", 1),
      sliderInput('point2', 'Epsilon', min=1, max=3,value=2, step=0.01, round=0),
      sliderInput('point3', 'Alpha', min=-2, max=-1,value=-1.5, step=0.001, round=0),
      sliderInput('point4', 'Beta', min=0.5, max=2.5,value=1.5, step=0.01, round=0),
      sliderInput('point5', 'Gamma', min=1, max=5,value=1, step=1, round=0),
      sliderInput('point8', 'Tau', min=1, max=20,value=10, step=1, round=0),
      numericInput("point6", "Poids final",3600,min=2000,max=5000),
      numericInput("point7", "Nombre de jour", 55,min=1,max=180)  
      
  
      
      ), 
    
    mainPanel(   
                 plotOutput("myplot"),
                 tabsetPanel(type = "tabs", 
                                      tabPanel("Croissance - Consomation", plotOutput("plot")), 
                                      tabPanel("Summary", verbatimTextOutput("summary")), 
                                      tabPanel("Table", tableOutput("table"))
                            )
             ) 
 )
)) 