
// let data = [{'id':'HN','name':'Ha Noi','data':[10,500,20,193,21,22,32]},
//             {'id':'HC','name':'Ho Chi Minh City','data':[10,4000,20,193,21,22,32]},
//             {'id':'DA','name':'Da Nang City','data':[10,300,20,193,21,22,32]},
//             {'id':'BI','name':'Binh Duong','data':[10,200,20,193,21,22,32]}];
let data = {'HN':{'name':'Ha Noi','data':[1000,200,300]},
            'HC':{'name':'Ho Chi Minh City','data':[1000,0,200,300]},
            'DA':{'name':'Da Nang City','data':[2000,2001,300]},
            'BI':{'name':'Binh Duong','data':[1500,200,300]}}
// A URL returns JSON data.
var url = "http://localhost:5000/region-job";
 
// let obj = fetch(url).then(function(response) {
//   return response.json();
// });
async function fetchMoviesJSON() {
  const response = await fetch(url);
  const data = await response.json();
  let oOffsets = {
    RP: [15, -15]
  };
  
  let _r_ = function (min, max) {
    return Math.round(min + (max - min) * Math.random());
  };
  
  let getNameById = function (sId) {
    let sName = 'N/A';
    if (data[sId]){
      sName = data[sId]['name'];
    }
    return sName;
  };
  
  let oCacheDataArea = {};
  let getRandomDataArea = function (sId) {
    if (oCacheDataArea[sId]) {
      return oCacheDataArea[sId];
    }
    let aValues = [
      [],
      [],
      [],
      []
    ];
    if (data[sId]){
      for (let i = 0; i < 4; i++) {
        let v0 = _r_(5, 15);
        let v1 = _r_(25, 35);
        let v3 = _r_(5, 10);
        let v2 = 100 - v0 - v1 - v3;
        aValues[0].push(v0);
        aValues[1].push(v1);
        aValues[2].push(v2);
        aValues[3].push(v3);
      }
    }
    oCacheDataArea[sId] = aValues;
    return aValues;
  };
  console.log(oCacheDataArea)
  // console.log(data.length);
  let oCacheDataPop = {};
  // console.log('BI' == data[3]['id']);
  let getRandomDataPop = function (sId) {
    if (oCacheDataPop[sId]) {
      return oCacheDataPop[sId];
    }
    let aValues = [];
    // let iPop = ZC._r_(2000000, 8000000);
    // for (let i = 0; i < data.length; i++) {
    //   aValues.push(iPop);
    //   iPop += _r_(-20000, 20000);
    // }
    if(data[sId]){
      for (let i = 0; i < data[sId]['data'].length; i++) {
        aValues.push(data[sId]['data'][i]);
      }
    }
    oCacheDataPop[sId] = [aValues];
    return [aValues];
  
  };
  
  console.log(oCacheDataPop);
  
  let updateAreaPopCharts = function (sId) {
    zingchart.exec('myChart', 'setdata', {
      graphid: 'gmap',
      data: getMapData(sId),
      update: false
    });
    zingchart.exec('myChart', 'modify', {
      graphid: 'histarea',
      data: {
        subtitle: {
          text: getNameById(sId)
        }
      },
      update: false
    });
    zingchart.exec('myChart', 'modify', {
      graphid: 'histpop',
      data: {
        subtitle: {
          text: getNameById(sId)
        }
      },
      update: false
    });
    zingchart.exec('myChart', 'setseriesvalues', {
      graphid: 'histarea',
      values: getRandomDataArea(sId),
      update: false
    });
    zingchart.exec('myChart', 'setseriesvalues', {
      graphid: 'histpop',
      values: getRandomDataPop(sId),
      update: false
    });
    zingchart.exec('myChart', 'update');
  }
  
  // zingchart.bind('myChart', 'node_click', function (p) {
  //   if (p.graphid.indexOf('zc-graph-pie') === 0) {
  //     updateAreaPopCharts(p.graphid.replace('zc-graph-pie', ''));
  //   }
  // });
  zingchart.bind('myChart', 'shape_click', function (p) {
    if (p.shape.mapItem) {
      updateAreaPopCharts(p.shape.id);
    }
  });
  
  
  
  var getMapData = function (sId) {
    let oGraphMainMap = {
      backgroundColor: 'none',
      x: '0px',
      y: '0px',
      width: '800px',
      height: '600px',
      type: 'null',
      id: 'gmap',
      title: {
        align: 'left',
        fontSize: '15px',
        paddingLeft: '20px',
        text: 'Interactive job visualization (*)'
      },
      source: {
        text: '(*) random data',
        offsetX: '-350px'
      },
      shapes: [{
        type: 'zingchart.maps',
        options: {
          x: '0px',
          y: '20px',
          width: '480px',
          height: '580px',
          id: 'mapvnm',
          name: 'vnm',
          zooming: true,
          panning: false,
          scrolling: false,
          scale: true,
          style: {
            controls: {
              visible: false
            },
            label: {
              visible: false
            },
            backgroundColor: '#f9f9f9',
            borderColor: '#666',
            hoverState: {
              visible: false
            },
            items: {}
          }
        }
      }]
    };
    oGraphMainMap.shapes[0].options.style.items[sId] = {
      backgroundColor: '#eeeeee #c2edc3'
    };
    return oGraphMainMap;
  };
  
  let aAreaValues = getRandomDataArea('HN');
  console.log(aAreaValues)
  let oGraphHistoryArea = {
    id: 'histarea',
    backgroundColor: 'none',
    x: '480px',
    y: '60px',
    width: '300px',
    height: '200px',
    type: 'bar',
    stacked: true,
    title: {
      fontSize: '14px',
      text: 'Job data of category distribution (*)'
    },
    subtitle: {
      fontSize: '12px',
      offsetY: '-5px',
      text: getNameById('HN')
    },
    source: {
      text: '(*) random data'
    },
    plotarea: {
      margin: '55 5 35 35'
    },
    scaleX: {
      values: '1:5:1',
      maxItems: 99,
      itemsOverlap: true,
      item: {
        fontSize: '9px'
      }
    },
    tooltip: {
      text: '%plot-text in %scale-key-text: %node-value%'
    },
    scaleY: {
      format: '%v%',
      item: {
        fontSize: '10px'
      }
    },
    plot: {
      alpha: 0.75,
      animation: {
        speed: 200,
        effect: 'ANIMATION_FADE_IN',
        method: 'ANIMATION_LINEAR',
        sequence: 'ANIMATION_BY_NODE'
      }
    },
    series: [{
      backgroundColor: '#D87676',
      values: aAreaValues[0],
      text: 'Software'
    },
    {
      backgroundColor: '#56b556',
      values: aAreaValues[1],
      text: 'Hardware'
    },
    {
      backgroundColor: '#e5e510',
      values: aAreaValues[2],
      text: 'Bussiness'
    },
    {
      backgroundColor: '#999',
      values: aAreaValues[3],
      text: 'Other'
    }
    ]
  };
  
  let aPopValues = getRandomDataPop('HN');
  console.log(aPopValues);
  let oGraphHistoryPop = {
    id: 'histpop',
    backgroundColor: 'none',
    x: '480px',
    y: '280px',
    width: '300px',
    height: '200px',
    type: 'area',
    title: {
      fontSize: '14px',
      text: 'Historic data of recruitment size (*)'
    },
    subtitle: {
      fontSize: '12px',
      offsetY: '-5px',
      text: getNameById('HN')
    },
    source: {
      text: '(*) random data'
    },
    plotarea: {
      margin: '55 5 35 35'
    },
    tooltip: {
      short: true,
      decimals: 4,
      text: 'Population in %scale-key-text: %node-value'
    },
    scaleX: {
      values: '1:12:1',
      maxItems: 99,
      itemsOverlap: true,
      item: {
        fontSize: '9px'
      }
    },
    scaleY: {
      minValue: 'auto',
      short: true,
      decimals: 2,
      item: {
        fontSize: '10px'
      }
    },
    plot: {
      alpha: 0.75,
      animation: {
        speed: 200,
        effect: 'ANIMATION_FADE_IN',
        method: 'ANIMATION_LINEAR',
        sequence: 'ANIMATION_BY_NODE'
      }
    },
    series: [{
      lineColor: '#333',
      backgroundColor: '#333 #fff',
      marker: {
        type: 'diamond',
        backgroundColor: '#666'
      },
      values: aPopValues
    }]
  };
  
  let oGraphLegend = {
    id: 'pielegend',
    type: 'pie',
    x: '480px',
    y: '500px',
    width: '300px',
    height: '60px',
    backgroundColor: 'none',
    plotarea: {
      margin: '2px'
    },
    plot: {
      flat: true,
      maxTrackers: 0,
      detach: false,
      alpha: 0.6,
      borderWidth: '0px',
      valueBox: {
        placement: 'out',
        offsetR: -25,
        align: 'left',
        text: '%plot-text',
        fontSize: '10px',
        fontWeight: 'bold',
        color: '#333',
        connector: {
          visible: false
        }
      }
    },
    tooltip: {
      visible: false
    },
    scale: {
      sizeFactor: 0.8
    },
    series: [{
      text: 'Software',
      values: [1],
      backgroundColor: '#d15c5c'
    },
    {
      text: 'Hardware',
      values: [1],
      backgroundColor: '#56b556'
    },
    {
      text: 'Bussiness',
      values: [1],
      backgroundColor: '#e5e510'
    },
    {
      text: 'Other',
      values: [1],
      backgroundColor: '#999'
    }
    ]
  };
  
  let chartConfig = {
    flat: true,
    backgroundColor: '#f3f3f3 #e3e3e3',
    borderColor: '#999',
    borderWidth: '1px',
    graphset: [
      getMapData('HN'),
      oGraphHistoryArea,
      oGraphHistoryPop,
      oGraphLegend
    ]
  };
  
  let bInit = true;
  zingchart.bind('myChart', 'load', function () {
    if (bInit) {
      bInit = false;
    }
  });
  
  
  
  zingchart.DEV.MAPSONBOTTOM = 1;
  // renders chart
  zingchart.loadModules('maps, maps-vnm', function (e) {
    zingchart.render({
      id: 'myChart',
      data: chartConfig,
      height: '100%',
      width: '100%'
    });
  });
};
fetchMoviesJSON();


// better placement to avoid pie overla
