import refined_stats as rs
import batch_2_comp as bc 
import os 


#Creating the common User Section 
user_info_html="""
    <div class="user_section" id="User_info">
        <h1 style="margin-left: 514px; width: 50%; height: 20px;">User Information</h1>
        <p style="margin-left: 514px; width: 50%; font-size: 17px;">
        Username: {0}<br>
        Email: {1}<br>
        Date: {2}<br>
        Time: {3}<br>
        </p>
    </div>

""".format(rs.full_user_name, rs.email, rs.Date, rs.Time)



## If more than 1 batch is selected 
if len(bc.main_window.batch_results) > 1:

    ## Creating links to the individual batches 
    links_html = '<table style="border-collapse: collapse; width: 40%; margin-top: 40px; margin-left: 90px;">'
    links_html += '<tr><th style="padding: 15px; border: 1px solid black;  background-color:lightblue; font-size :24px;">Batch Name</th><th style="padding: 15px; border: 1px solid black; background-color:lightblue; font-size: 24px;">Report Link</th></tr>'

    for html_file_path in bc.html_file_paths:
        for folder_path in bc.folder_name_paths:
            if os.path.basename(str(html_file_path)).startswith(os.path.basename(str(folder_path))):
                batch_name = os.path.basename(str(folder_path))
                report_link = '<a href="' + ''.join(html_file_path) + '" target="_blank">Click here to view the report</a>'
                links_html += f'<tr><td style="padding: 10px; border: 1px solid black;text-align: center; font-size: 20px;">{batch_name}</td><td style="padding: 10px; border: 1px solid black;text-align: center; font-size: 20px;">{report_link}</td></tr>'

    links_html += '</table>'


    #The Quick Links Section
    toc_html = f"""
    <div class="quick-links">
    <nav>
            <a href="#Detection-results">Detection Results</a>
            <a href="#statistics-summary">Statistics Summary</a>
    </nav>
    </div>
    """


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
                <div class="flex-item" style="flex-basis: 50%; margin-left:370px; margin-top:70px;">{0}</div>
                </div>
            </div>
            
            <div id="stats-container" style="display: none;">
                <a id="stats-graph"></a>
                <div class="flex-item" style="flex-basis: 50%;  margin-left:370px; margin-top:70px;">{1}</div>
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
        """.format(rs.img_tags['bee_counts.png'], rs.img_tags['descriptive_stats.png'])


    ## Section 3 : The normality section 

    section3_html = """

            <div class="section1" id="statistics-summary">
                <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;"> Normality Checks</h1>
                <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> QQ-Plot </h1>
                <div class="QQ-Plot" style="margin-left:370px; margin-top:50px;">{0}</div>   
                <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Shapiro-Wilk Test </h1>
                <div class="Shapiro-Wilk Test" style="width:600px; margin-left:90px; margin-top:50px;">{1}</div> 
                <div class="Shapiro-Wilk Test" style="width:770px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{2}</div> 
                <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Statistics Summary</h1>
            </div>
        """.format(rs.img_tags['QQ-plot.png'], rs.html0, bc.Output1)



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
            if bc.p_value < 0.05:
                parametric_html = """
                
                <div class="section1" id="statistics-summary">
                        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Performing ONE-way ANOVA </h1>
                        <div class="ANOVA test " style="margin-left:90px; margin-top:40px;">{0}</div>   
                        <div class="ANOVA test " style="width:950px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                        <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Post Hoc Tukey Test </h1>
                        <div class="Tukey test" style="margin-left:90px; margin-top:50px;">{2}</div>   
                        <h1 style="margin-left: 60px; margin-top: 50px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Visualisation </h1>        
                        <div class="flex-item" style="flex-basis: 100%; margin-top:70px; margin-left:370px;">{3}</div>
                        
                
                </div>
                """.format(rs.html5, bc.Conclusion2, rs.html6, rs.img_tags['Boxplot.png'])

            else:
                parametric_html = """
                
                <div class="section1" id="statistics-summary">
                        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Performing ONE-way ANOVA </h1>
                        <div class="ANOVA test " style="margin-left:90px; margin-top:40px;">{0}</div>   
                        <div class="ANOVA test " style="width:950px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                </div>
                """.format(rs.html5, bc.Conclusion2)


    else:

    ## Section 5 : The non-parametric section 

        if len(bc.main_window.batch_results)==2:
            non_parametric_html = """

                <div class="section1" id="statistics-summary">
                    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Mann Whitney- U Test </h1>
                    <div class="Mann Whitney- U Test " style="margin-left:90px; margin-top:50px;">{0}</div>  
                    <div class="Mann Whitney- U Test " style="width:800px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                </div>
            """.format(rs.html7, bc.Conclusion3)

        if len(bc.main_window.batch_results)>2:

            if bc.krushal_p<0.05:
                non_parametric_html = """

                    <div class="section1" id="statistics-summary">
                        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Krushal-Wallis Test </h1>
                        <div class="Krushal-Wallis Test " style="margin-left:90px; margin-top:50px;">{0}</div>  
                        <div class="Krushal-Wallis Test" style="width:600px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Dunn's Test </h1>
                        <div class="Dunn's Test" style="margin-left:90px; margin-top:50px;">{2}</div>  
                    </div>
                """.format(rs.html8, bc.Conclusion4, rs.html9)

            else:
                non_parametric_html = """

                    <div class="section1" id="statistics-summary">
                        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Krushal-Wallis Test </h1>
                        <div class="Krushal-Wallis Test " style="margin-left:90px; margin-top:50px;">{0}</div>  
                        <div class="Krushal-Wallis Test" style="width:600px; margin-left:90px; margin-top:50px; background-color: lightgrey; font-size: 21px;">{1}</div> 
                    </div>
                """.format(rs.html8, bc.Conclusion4)


    link_heading = """
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;"> Links to Individual Batches </h1>
    """

else: 

    # Contains the Model Summary 
    if os.path.exists(os.path.join(rs.model_path, 'opt.yaml')):
        section3_html = """
        
            <div class="section2" id="Model-summary">
                <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Optimized Parameters for YOLO Model Performance</h1>
            </div>


            <div class="flex-container" style="margin-left:200px; margin-top:30px;">
                <div class="flex-item" style="flex-basis: 100%;">{0}</div>
            </div>""".format(rs.html_summary)
        
    else:
        section3_html = " "

        
    # Creating section for the performance graphs that were provided

    graph_html_list = []
    for img_tag, img_name in zip(rs.perform_graphs, rs.perform_graphs_names):
        image_name = os.path.splitext(img_name)[0]
        graph_html_list.append(
            """
            <div class="graph-container" style="margin: 20px;">
                <h1 style="margin-left: 100px; margin-top: 10px; font-size: 20px; padding: 10px; background-color: lightblue;">{}</h1>
                <div class="flex-item" style="flex-basis: 100%; margin-top: 10px; margin-left: 200px; ">{}</div>
            </div>
            """.format(image_name, img_tag)
        )

    # Join the HTML code for each image into a single string
    graphs_html = '\n'.join(graph_html_list)

    if len(graph_html_list)>0:
        section4_html = """
        <a id="model-summary"></a>
        <div class="section2" id="Model-summary">
            <h1 style="margin-left: 60px; margin-top: 60px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Performance Graphs for YOLO Model Training</h1>
        </div>

        <div id="plot-container" style="display: flex; flex-wrap: wrap;">
            {}
        </div>

        """.format(graphs_html)
    else:
        section4_html = " "


    # Creating the Model Summary header depending whether either section 3 or 4 is present or not 
    
    model_summary_header = ''
    if section3_html or section4_html:
        model_summary_header = '<a id="model-summary"></a>''<h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Model Summary</h1>'

    # This section is displayed when the input folder/image does not have any detections 
    if not bool(bc.filtered_counts):

        #Quick links section
        toc_html = f"""
            <div class="quick-links">
            <nav>
                <a href="#Detection-results">Detection Results</a>
                <a href="#model-summary">Model Summary</a>
            </nav>
            </div>
            """
        
        # Detection results section
        image_path = os.path.join(os.getcwd(), 'resources', 'no_detections.png')
        no_detect_html = f"""
            <a id="Detection-results"></a>
            <div class="no-detections">
                <h1 style="margin-left: 10px; margin-top: 50px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Detection Results</h1>
                <p style="margin-left:100px; margin-top: 40px; margin-bottom:-20;"><img src="{image_path}" style="width: 600px; height: 130px;" /></p>
            </div>
        """

    else:
    
        # The quick links section 
        toc_html = f"""
            <div class="quick-links">
            <nav>
                    <a href="#output-examples">Output Examples</a>
                    <a href="#Detection-results">Detection Results</a>
                    <a href="#model-summary">Model Summary</a>
            </nav>
            </div>
            """

        
        #Heading contains the title of the sub-section
        heading_html = """
        <a id="output-examples"></a>
        <div class="section2" id="Output Examples">
            <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Output Examples</h1>
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Detection of Bees using YOLO Model</h1>
        </div>
            """


        #Section 1 contains the output example images 
        section1_html = '<div style="display: flex; flex-wrap: wrap; margin-top: 30px;">'
        for i, path in enumerate(rs.img_tags_list):
        
            # Extract subfolder name from image path
            subfolder_name = os.path.basename(os.path.dirname(path))
            section1_html += f'{path}'

        section1_html += '</div>'


        # Section 2 contains the detection results 
        section2_html="""
        <a id="Detection-results"></a>
        <div class="section1" id="Detection-results">
            <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Detection Results</h1>
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Species Counts and Abundance Summary</h1>
        </div>


        <div class="flex-container" style="margin-left:200px; margin-top:70px;">
            <div class="flex-item" style="flex-basis: 50%;">{0}</div>
            <div class="flex-item" style="flex-basis: 50%;">{1}</div>
        </div>

        
        <div class="section1" id="Detection-results">
            <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Visualizing Species Counts and Abundance</h1>
        </div>

        
        <div class="flex-container" style="margin-left:150px; width:1600px; margin-top: 50px;">
        <div class="flex-item" style="flex-basis: 50%;">{2}</div>
        <div class="flex-item" style="flex-basis: 50%;">{3}</div>
        </div>
        """.format(rs.html_counts,rs.html_abundance,rs.img_tags['Bar_plot.png'],rs.img_tags['bee_species_counts.png'])


# Setting the HTML Layout 
if not bool(bc.filtered_counts):
    html = f"""
    <html>
    <head>
        <title> Statistics Report</title>
            <style>
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: lightblue;
                    padding: 10px;
                    flex-shrink: 0;
                    
                }}

                .flex-container {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }}

                .flex-item {{
                    margin-left: -98px;
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
        {no_detect_html}
        {model_summary_header}
        {section3_html}
        {section4_html}

    </body>
    </html>""" 

    with open('stats.html', "w") as f:
        f.write(html)


   
else:    
    if len(bc.main_window.batch_results) == 1:

        html = f"""
        <html>
        <head>
            <title> Statistics Report</title>
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
        {model_summary_header}
        {section3_html}
        {section4_html}

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
                <title> Statistics Report</title>
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

                        .Graph-links nav a {{
                            text-align: center;
                            padding: 16px 18px;
                            background-color: lightblue; 
                            color: black !important;
                            font-size: 20px;
                        
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
            {link_heading}
            {links_html}

        </body>
        </html>""" 

        else:

            html = f"""
            <html>
            <head>
                <title> Statistics Report</title>
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
            {link_heading}
            {links_html}

            </body>
            </html>""" 

        with open('Batch_Comparison.html', "w") as f:
            f.write(html)
