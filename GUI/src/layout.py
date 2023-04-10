import refined_stats as rs
import batch_2_comp as bc 
import os 

# HTML Layout for 1 batch
if len(bc.main_window.batch_results) == 1:
    print(bc.main_window.batch_results)


    toc_html = f"""
        <div class="quick-links">
        <nav>
                <a href="#output-examples">Output Examples</a>
                <a href="#Detection-results">YOLO Results</a>
                <a href="#model-summary">Model Summary</a>
        </nav>
        </div>
        """


    #The User Information section
    user_info_html="""
        <div class="user_section" id="User_info">
            <h1 style="margin-left: 534px; width: 50%; height: 20px;">User Information</h1>
            <p style="margin-left: 420px; width: 50%; font-size: 17px;">
            Username: {0}<br>
            Email: {1}<br>
            Date: {2}<br>
            Time: {3}<br>
            </p>
        </div>

    """.format(rs.full_user_name, rs.email, rs.Date, rs.Time)

    
    #Section 1 contains the output example images 
    heading_html = """
    <a id="output-examples"></a>
    <div class="section2" id="Output Examples">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Output Examples</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Detection of Bees using YOLO</h1>
    </div>
        """

    section1_html = '<div style="display: flex; flex-wrap: wrap; margin-top: 60px;">'
    for i, path in enumerate(rs.random_image_paths):
    
        # Extract subfolder name from image path
        subfolder_name = os.path.basename(os.path.dirname(path))
        section1_html += f'<p style="margin-left: 165px;"><img src="{path}" title="{subfolder_name}" width="500" height="500"></p>'

    section1_html += '</div>'
    

    
    # Section 2 contains the detection results 
    section2_html="""
    <a id="yolo-results"></a>
    <div class="section1" id="Detection-results">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">YOLO Results</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Species Counts and Abundance Summary</h1>
    </div>


    <div class="flex-container" style="margin-left:200px; margin-top:70px;">
        <div class="flex-item" style="flex-basis: 50%;">{0}</div>
        <div class="flex-item" style="flex-basis: 50%;">{1}</div>
    </div>

    
    <div class="section1" id="Detection-results">
        <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Visualizing Species Counts and Abundance</h1>
    </div>

    
    <div class="flex-container" style="margin-left:150px; width:1200px; margin-top: 50px;">
        <div class="flex-item" style="flex-basis: 50%;"><img src="{2}/Bar_plot.png" style="width: 600px; height: 500px;">
        </div>
        <div class="flex-item" style="flex-basis: 50%;">
            <img src="{2}/bee_species_counts.png" style="width: 650px; height: 600px;">
        </div>
    </div> """.format(rs.html_counts,rs.html_abundance,rs.output_directory_single_batch)


    section3_html = """
    
    
    <a id="model-summary"></a>
    <div class="section2" id="Model-summary">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Model Summary</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Optimized Parameters for YOLO Model Performance</h1>
    </div>


    <div class="flex-container" style="margin-left:200px; margin-top:60px;">
        <div class="flex-item" style="flex-basis: 100%;">{0}</div>
    </div>

    
    <div class="section2" id="Model-summary">
        <h1 style="margin-left: 60px; margin-top: 90px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Performance Graphs for YOLO Model Training</h1>
    </div>

    <div class="section2">
         <div><p style="margin-left: 180px; margin-top: 100px;"><img src="{1}/{2}/results.png" width="1000" height="1000"></p></div>
         <div><p style="margin-left: 180px; margin-top: 100px;"><img src="{1}/{2}/F1_curve.png" width="1000" height="1000"></p></div>
         <div><p style="margin-left: 55px; margin-top: 100px;"><img src="{1}/{2}/confusion_matrix.png" width="1000" height="1000"></p></div>
    </div>
    
    """.format(rs.html_summary, bc.main_window.Models.path, bc.main_window.ui.comboBox.currentText())


# HTML layout for more than two batches
else: 

    #The Quick Links Section
    toc_html = f"""
    <div class="quick-links">
    <nav>
            <a href="#Detection-results">Detection Results</a>
            <a href="#statistics-summary">Statistics Summary</a>
    </nav>
    </div>
    """

    #The User Information section
    user_info_html="""
        <div class="user_section" id="User_info">
            <h1 style="margin-left: 534px; width: 50%; height: 20px;">User Information</h1>
            <p style="margin-left: 420px; width: 50%; font-size: 17px;">
            Username: {0}<br>
            Email: {1}<br>
            Date: {2}<br>
            Time: {3}<br>
            </p>
        </div>

    """.format(rs.full_user_name, rs.email, rs.Date, rs.Time)



    # Contains all the statistic results 

    section1_html = """
        <a id="Detection-results"></a>
        <div class="section1" id="Detection-results">
            <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Detection Results</h1>
            <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Species Counts </h1>

            <div class="flex-item" style="flex-basis: 100%; margin-left:220px; margin-top:50px;">{0}</div>

            <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Descriptive Statistics </h1>
            <div class="flex-item" style="flex-basis: 100%; margin-left:220px; margin-top: 50px;">{1}</div>
        
        <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Visualisation </h1>        
        
        """.format(rs.html1,rs.html2)



    section2_html ="""
        <div class="Graph-links">
            <nav>
                <a href="#" class="graph-link" data-target="counts-graph">View Bee Counts</a>
                <a href="#" class="graph-link" data-target="stats-graph">View Descriptive Statistics</a>
            </nav>
            </div>

            <div id="plot-container">
            <div id="counts-container">
                <a id="counts-graph"></a>
                <div class="flex-item" style="flex-basis: 100%; margin-top:70px;"> 
                <p style ="margin-left: 370px;"><img src="{0}/bee_counts.png" width="800" height="600"></p>
                </div>
            </div>
            
            <div id="stats-container" style="display: none;">
                <a id="stats-graph"></a>
                <div class="flex-item" style="flex-basis: 100%; margin-top:70px;"> 
                <p style ="margin-left: 370px;"><img src="{0}/descriptive_stats.png" width="800" height="600"></p>
                </div>
            </div>
            </div>

                <script>
                    // Add click event listener to graph links
                    $('.graph-link').click(function(event) {{
                        event.preventDefault();  // Prevent default link behavior

                        // Get the ID of the target div from the data-target attribute
                        var target = $(this).data('target');

                        // Show the selected container and hide the other one
                        if (target == 'counts-graph') {{
                        $('#counts-container').show();
                        $('#stats-container').hide();
                        }} else {{
                        $('#stats-container').show();
                        $('#counts-container').hide();
                        }}
                    }});
                </script>
        </div>
        """.format(rs.output_directory_batch_comparison)


    ## Section 3 : The normality section 

    section3_html = """

            <div class="section1" id="statistics-summary">
                <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;"> Normality Checks</h1>
                <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> QQ-Plot </h1>
                <div class="QQ-Plot" style="margin-left:270px; margin-top:50px;"> <p><img src="{0}/QQ-plot.png" width="800" height="600"></p></div>   
                <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Shapiro-Wilk Test </h1>
                <div class="Shapiro-Wilk Test" style="width:600px; margin-left:90px; margin-top:50px;">{1}</div> 
                <div class="Shapiro-Wilk Test" style="width:770px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{2}</div> 
                <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Statistics Summary</h1>
            </div>
        """.format(rs.output_directory_batch_comparison, rs.html0, bc.Output1)



    ## Section 4 : The parametric section 


    if bc.p > bc.alpha:
        if len(bc.main_window.batch_results)==2:
            parametric_html = """

                
                <div class="section1" id="statistics-summary">
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Levene's Test - Checking Equality of Variance</h1>
                    <div class="Levene's-test" style="margin-left:90px; margin-top:50px;">{0}</div>   
                    <div class="Levene's-test" style="width:600px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                    <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Independent T-Test</h1>
                    <div class="t-test" style="margin-left:90px; margin-top:50px;">{2}</div>   
                    <div class="t-test" style="width:950px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{3}</div> 
                </div>
            """.format(rs.html3, bc.Output2, rs.html4, bc.Conclusion1)


        else:
            parametric_html = """
            
            <div class="section1" id="statistics-summary">
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Performing ONE-way ANOVA </h1>
                    <div class="ANOVA test " style="margin-left:90px; margin-top:40px;">{0}</div>   
                    <div class="ANOVA test " style="width:950px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                    
                    <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Post Hoc Tukey Test </h1>
                    <div class="Tukey test" style="margin-left:90px; margin-top:50px;">{2}</div>   


                <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Visualisation </h1>        

                <div class="Graph-links">
                <nav>
                    <a href="#" class="graph-link" data-target="boxplot-graph">View Boxplot</a>
                    <a href="#" class="graph-link" data-target="heatmap-graph">View Heatmap</a>
                </nav>
                </div>

                <div id="plot-container">
                <div id="boxplot-container">
                    <a id="boxplot-graph"></a>
                    <div class="flex-item" style="flex-basis: 100%; margin-top:70px;"> 
                    <p style ="margin-left: 370px;"><img src="{3}/Boxplot.png" width="800" height="600"></p>
                    </div>
                </div>
                
                <div id="heatmap-container" style="display: none;">
                    <a id="heatmap-graph"></a>
                    <div class="flex-item" style="flex-basis: 100%; margin-top:70px;"> 
                    <p style ="margin-left: 370px;"><img src="{3}/Heatmap.png" width="800" height="600"></p>
                    </div>
                </div>
                </div>

                    <script>
                        // Add click event listener to graph links
                        $('.graph-link').click(function(event) {{
                            event.preventDefault();  // Prevent default link behavior

                            // Get the ID of the target div from the data-target attribute
                            var target = $(this).data('target');

                            // Show the selected container and hide the other one
                            if (target == 'boxplot-graph') {{
                            $('#boxplot-container').show();
                            $('#heatmap-container').hide();
                            }} else {{
                            $('#heatmap-container').show();
                            $('#boxplot-container').hide();
                            }}
                        }});
                    </script>
            </div>
            """.format(rs.html5, bc.Conclusion2, rs.html6, rs.output_directory_batch_comparison)

    else:

    ## Section 5 : The non-parametric section 

        if len(bc.main_window.batch_results)==2:
            non_parametric_html = """

                <div class="section1" id="statistics-summary">
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Mann Whitney- U Test </h1>
                    <div class="Mann Whitney- U Test " style="margin-left:90px; margin-top:50px;">{0}</div>  
                    <div class="Mann Whitney- U Test " style="width:600px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                </div>
            """.format(rs.html7, bc.Conclusion3)

        else:
            non_parametric_html = """

                <div class="section1" id="statistics-summary">
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Krushal-Wallis Test </h1>
                    <div class="Krushal-Wallis Test " style="margin-left:90px; margin-top:50px;">{0}</div>  
                    <div class="Krushal-Wallis Test" style="width:600px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Dunn's Test </h1>
                    <div class="Dunn's Test" style="margin-left:90px; margin-top:50px;">{2}</div>  
                </div>
            """.format(rs.html8, bc.Conclusion4, rs.html9)

if len(bc.main_window.batch_results) == 1:

    html = f"""
            <html>
            <head>
                <title>YOLO Statistics Report</title>
                    <style>
                        .flex-container {{
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            }}

                        .flex-item {{
                            margin-left: -98px;
                            }}

                        .header {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            background-color: lightblue;
                            padding: 10px;
                            flex-shrink: 0;
                            
                            }}

                        .user_section {{
                            text-align: right;
                            margin-right: 190px;
                            font-size: 15px;
                            flex-shrink: 0;
                            
                            }}    

                        .quick-links nav a {{
                            text-align: center;
                            padding: 14px 16px;
                            background-color:  #F5F5DC; 
                            color: black !important;
                            font-size: 24px;
                            
                            }}

                        .quick-links nav a:hover {{
                            background-color: lightgrey;
                            }} 


                        body {{
                            background-color: #F8F8FF;
                            }}    

                    </style>

            </head>
            <body>
            <div class="header">
                <h1> Statistics Report</h1>
                {user_info_html} 
            </div>     
                {toc_html}
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                        {heading_html}
                        {section1_html}
                        {section2_html}
                        {section3_html}

</body>
</html>""" 

    with open('stats.html', "w") as f:
        f.write(html)

else: 

    # Setting the html layout 
    if bc.p > bc.alpha:
        html = f"""
                <html>
                <head>
                    <title>YOLO Statistics Report</title>
                        <style>
                            .flex-container {{
                                display: flex;
                                align-items: center;
                                justify-content: space-between;
                                }}

                            .flex-item {{
                                margin-left: -98px;
                                }}

                            .header {{
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                background-color: lightblue;
                                padding: 10px;
                                flex-shrink: 0;
                                
                                }}

                            .user_section {{
                                text-align: right;
                                margin-right: 190px;
                                font-size: 15px;
                                flex-shrink: 0;
                                
                                }}    

                            .quick-links nav a {{
                                text-align: center;
                                padding: 14px 16px;
                                background-color:  #F5F5DC; 
                                color: black !important;
                                font-size: 24px;
                                
                                }}

                            .Graph-links nav a {{
                                text-align: center;
                                padding: 16px 18px;
                                background-color: lightblue; 
                                color: black !important;
                                font-size: 20px;
                                
                                }}

                            .quick-links nav a:hover {{
                                background-color: lightgrey;
                                }} 

                            .Graph-links nav a:hover {{
                                background-color: lightgrey;
                                }} 

                            .Graph-links nav {{
                                margin-left: 70px;
                                margin-top: 30px;
                                }}

                            body {{
                                background-color: #F8F8FF;
                                }}    

                        </style>

                </head>
                <body>
                <div class="header">
                    <h1> Statistics Report</h1>
                    {user_info_html} 
                </div>     
                    {toc_html}
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                            {section1_html}
                            {section2_html}
                            {section3_html}
                            {parametric_html}

    </body>
    </html>""" 

    else:

        html = f"""
            <html>
            <head>
                <title>YOLO Statistics Report</title>
                    <style>
                        .flex-container {{
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            }}

                        .flex-item {{
                            margin-left: -98px;
                            }}

                        .header {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            background-color: lightblue;
                            padding: 10px;
                            flex-shrink: 0;
                            
                            }}

                        .user_section {{
                            text-align: right;
                            margin-right: 190px;
                            font-size: 15px;
                            flex-shrink: 0;
                            
                            }}    

                        .quick-links nav a {{
                            text-align: center;
                            padding: 14px 16px;
                            background-color:  #F5F5DC; 
                            color: black !important;
                            font-size: 24px;
                            
                            }}

                        .Graph-links nav a {{
                            text-align: center;
                            padding: 16px 18px;
                            background-color: lightblue; 
                            color: black !important;
                            font-size: 20px;
                            
                            }}

                        .quick-links nav a:hover {{
                            background-color: lightgrey;
                            }} 

                        .Graph-links nav a:hover {{
                            background-color: lightgrey;
                            }} 

                        .Graph-links nav {{
                            margin-left: 70px;
                            margin-top: 30px;
                            }}

                        body {{
                            background-color: #F8F8FF;
                            }}    

                    </style>

            </head>
            <body>
            <div class="header">
                <h1> Statistics Report</h1>
                {user_info_html} 
            </div>     
                {toc_html}
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                        {section1_html}
                        {section2_html}
                        {section3_html}
                        {non_parametric_html}

    </body>
    </html>""" 

    with open('Batch_Comparison.html', "w") as f:
        f.write(html)
