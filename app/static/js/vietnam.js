var d3, document, console;

var width = 960,
    height = 750;

var svg = d3.select("container").append("svg")
    .attr("width", width)
    .attr("height", height)
   // .style("display", block)
   // .style("margin", auto);

var color = d3.scaleThreshold()
  .domain([1, 10, 50, 200, 500, 1000, 2000, 4000])
  .range(d3.schemeOrRd[9]);

var tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var projection = d3.geoMercator()
                   .scale(2600)
                    // Center the Map in Vietnam
                   .center([110, 16])
                   .translate([width/2, height/2]);

var path = d3.geoPath(projection);

 var g = svg.append("g")
            .attr("class", "key")
            .attr("transform", "translate(0, 40)");

var x = d3.scaleSqrt()
        .domain([0, 4500])
        .rangeRound([440, 950]);

g.append("text")
        .attr("class", "caption")
        .attr("x", x.range()[0])
        .attr("y", -6)
        .attr("fill", "#000")
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text("Population per square kilometer");

var switchPressed = false;

function changeData() {
    switchPressed = !switchPressed;
    
    
    if(switchPressed) {
        document.getElementById("title").innerHTML = "Vietnam Labour Force 15+ Years of Age, 2011";
        
        g.selectAll("rect")
          .data(color.range().map(function(d) {
              d = color.invertExtent(d);
              if (d[0] == null) d[0] = x.domain()[0];
              if (d[1] == null) d[1] = x.domain()[1];
              return d;
            }))
          .enter().append("rect")
            .attr("height", 8)
            .attr("x", function(d) { return x(d[0]); })
            .attr("width", function(d) { return x(d[1]) - x(d[0]); })
            .attr("fill", function(d) { return color(d[0]); });

        g.select("text")
            .attr("class", "caption")
            .attr("x", x.range()[0])
            .attr("y", -6)
            .attr("fill", "#000")
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text("Population per thousand persons");

        g.call(d3.axisBottom(x)
            .tickSize(13)
            .tickValues(color.domain()))
          .select(".domain")
            .remove();
    } else {
        document.getElementById("title").innerHTML = "Vietnam Population Density, 2011";
        
        g.selectAll("rect")
          .data(color.range().map(function(d) {
              d = color.invertExtent(d);
              if (d[0] == null) d[0] = x.domain()[0];
              if (d[1] == null) d[1] = x.domain()[1];
              return d;
            }))
          .enter().append("rect")
            .attr("height", 8)
            .attr("x", function(d) { return x(d[0]); })
            .attr("width", function(d) { return x(d[1]) - x(d[0]); })
            .attr("fill", function(d) { return color(d[0]); });

        g.select("text")
            .attr("class", "caption")
            .attr("x", x.range()[0])
            .attr("y", -6)
            .attr("fill", "#000")
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text("Population per square kilometer");

        g.call(d3.axisBottom(x)
            .tickSize(13)
            .tickValues(color.domain()))
          .select(".domain")
            .remove();
    }
    
    display();
    
}

display();

function display() {

    g.selectAll("rect")
        .data(color.range().map(function(d) {
            d = color.invertExtent(d);
            if (d[0] == null) d[0] = x.domain()[0];
            if (d[1] == null) d[1] = x.domain()[1];
            return d;
        }))
        .enter().append("rect")
        .attr("height", 8)
        .attr("x", function(d) { return x(d[0]); })
        .attr("width", function(d) { return x(d[1]) - x(d[0]); })
        .attr("fill", function(d) { return color(d[0]); });

//    g.append("text")
//        .attr("class", "caption")
//        .attr("x", x.range()[0])
//        .attr("y", -6)
//        .attr("fill", "#000")
//        .attr("text-anchor", "start")
//        .attr("font-weight", "bold")
//        .text("Population per square kilometer");

    g.call(d3.axisBottom(x)
        .tickSize(13)
        .tickValues(color.domain()))
      .select(".domain")
        .remove();


    d3.json("Vietnam.json", function(error, data) {

        if(error) console.error(data);

        console.log(data);
        
//        g.select("text")
//                .attr("class", "caption")
//                .attr("x", x.range()[0])
//                .attr("y", -6)
//                .attr("fill", "#000")
//                .attr("text-anchor", "start")
//                .attr("font-weight", "bold")
//                .text("Population per square kilometers");
            
        svg.selectAll("path")
           .data(data.features)
           .enter()
           .append("path")

           .attr("fill", function(d) { return color(d.properties.density);})
           .attr("stroke", "#000")
           .attr("stroke-opacity", 0.3)
           .attr("d", path)
           .on("mouseover", function(d) {
                tooltip.transition()
                        .duration(200)
                        .style("opacity", 0.9);
                tooltip.html(d.properties.NAME_1 + "<br/>" + 
                             "Density: " + d.properties.density)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY - 28) + "px")

           })
           .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
           })
        
        if(switchPressed) {
//            document.getElementById("title").innerHTML = "Vietnam Labour Force @ 15+ Years of Age, 2011";
//        
//            g.select("text")
//                .attr("class", "caption")
//                .attr("x", x.range()[0])
//                .attr("y", -6)
//                .attr("fill", "#000")
//                .attr("text-anchor", "start")
//                .attr("font-weight", "bold")
//                .text("Population per thousand persons");
            
            svg.selectAll("path")
               .data(data.features)
               // .enter()
               // .append("path")

               .attr("fill", function(d) {return color(d.properties.labour);})
               .attr("stroke", "#000")
               .attr("stroke-opacity", 0.3)
               .attr("d", path)
               .on("mouseover", function(d) {
                    tooltip.transition()
                            .duration(200)
                            .style("opacity", 0.9);
                    tooltip.html(d.properties.NAME_1 + "<br/>" + 
                                d.properties.labour)
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY - 28) + "px")

               })
               .on("mouseout", function(d) {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
               })

        } else {
            
//            document.getElementById("title").innerHTML = "Vietnam Population Density, 2011";
            
            svg.selectAll("path")
               .data(data.features)
               // .enter()
               // .append("path")

               .attr("fill", function(d) { return color(d.properties.density);})
               .attr("stroke", "#000")
               .attr("stroke-opacity", 0.3)
               .attr("d", path)
               .on("mouseover", function(d) {
                    tooltip.transition()
                            .duration(200)
                            .style("opacity", 0.9);
                    tooltip.html(d.properties.NAME_1 + "<br/>" + 
                                 d.properties.density)
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY - 28) + "px")

               })
               .on("mouseout", function(d) {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
               })
        }

    })


}