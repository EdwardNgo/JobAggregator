let data = [
    ['Ha Noi', 9, 48.5, 45.7, 38.3, 14.1, 'HN'],
    ['Ho Chi Minh City', 12, 49, 49.4, 35.0, 11.3, 'HC'],
    ['Da Nang City', 13.24, 52.5, 4.2, 18.3, 70.3, 'DA'],
    ['Binh Duong', 14, 51.8, 49.4, 35.4, 9.2, 'BI'],
  ];
  
  // better placement to avoid pie overlap
  let oOffsets = {
    RP: [15, -15]
  };
  
  let _r_ = function (min, max) {
    return Math.round(min + (max - min) * Math.random());
  };
  
  let getNameById = function (sId) {
    let sName = 'N/A';
    for (let i = 0; i < data.length; i++) {
      if (sId === data[i][6]) {
        sName = data[i][0];
      }
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
    for (let i = 0; i < data.length; i++) {
      let v0 = _r_(5, 15);
      let v1 = _r_(25, 35);
      let v3 = _r_(5, 10);
      let v2 = 100 - v0 - v1 - v3;
      aValues[0].push(v0);
      aValues[1].push(v1);
      aValues[2].push(v2);
      aValues[3].push(v3);
    }
    oCacheDataArea[sId] = aValues;
    return aValues;
  };
  
  let oCacheDataPop = {};
  let getRandomDataPop = function (sId) {
    if (oCacheDataPop[sId]) {
      return oCacheDataPop[sId];
    }
    let aValues = [];
    let iPop = ZC._r_(2000000, 8000000);
    for (let i = 0; i < data.length; i++) {
      aValues.push(iPop);
      iPop += _r_(-20000, 20000);
    }
    oCacheDataPop[sId] = [aValues];
    return [aValues];
  };
  
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
  
  zingchart.bind('myChart', 'node_click', function (p) {
    if (p.graphid.indexOf('zc-graph-pie') === 0) {
      updateAreaPopCharts(p.graphid.replace('zc-graph-pie', ''));
    }
  });
  zingchart.bind('myChart', 'shape_click', function (p) {
    if (p.shape.mapItem) {
      updateAreaPopCharts(p.shape.id);
    }
  });
  
  let addPieGraphs = function () {
    for (let i = 0; i < data.length; i++) {
      let info = data[i];
      let xy = zingchart.maps.getXY('mapvnm', [info[1], info[2]]);
      let oGraph = {
        id: 'pie' + info[6],
        type: 'pie',
        x: xy[0] - 80 + (oOffsets[info[6]] ? oOffsets[info[6]][0] : 0),
        y: xy[1] - 25 + (oOffsets[info[6]] ? oOffsets[info[6]][1] : 0),
        width: '160px',
        height: '50px',
        backgroundColor: 'none',
        plotarea: {
          margin: '2px'
        },
        plot: {
          detach: false,
          alpha: 0.75,
          borderWidth: '0px',
          valueBox: {
            visible: false
          }
        },
        title: {
          fontSize: '10px',
          offsetY: '40px',
          fontWeight: 'bold',
          text: info[0]
        },
        tooltip: {
          padding: '10px',
          fontSize: '13px',
          fontWeight: 'bold',
          text: '%node-value% in %plot-text'
        },
        series: [{
          text: 'Settlement Area',
          values: [info[5]],
          backgroundColor: '#d15c5c'
        },
        {
          text: 'Forest Area',
          values: [info[4]],
          backgroundColor: '#56b556'
        },
        {
          text: 'Agriculture',
          values: [info[3]],
          backgroundColor: '#e5e510'
        },
        {
          text: 'Other',
          values: [Number((100 - info[3] - info[4] - info[5]).toFixed(1))],
          backgroundColor: '#999'
        }
        ]
      };
      zingchart.exec('myChart', 'addgraph', {
        data: oGraph,
        update: false
      });
    }
    zingchart.exec('myChart', 'update');
  }
  
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
          zooming: false,
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
  
  let aAreaValues = getRandomDataArea(data[0][6]);
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
      text: getNameById(data[0][6])
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
  
  let aPopValues = getRandomDataPop(data[0][6]);
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
      text: 'Historic data of population size (*)'
    },
    subtitle: {
      fontSize: '12px',
      offsetY: '-5px',
      text: getNameById(data[0][6])
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
      values: '1:5:1',
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
      values: aPopValues[0]
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
      text: 'Settlement Area',
      values: [1],
      backgroundColor: '#d15c5c'
    },
    {
      text: 'Forest Area',
      values: [1],
      backgroundColor: '#56b556'
    },
    {
      text: 'Agriculture',
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
      getMapData(data[0][6]),
      oGraphHistoryArea,
      oGraphHistoryPop,
      oGraphLegend
    ]
  };
  
  let bInit = true;
  zingchart.bind('myChart', 'load', function () {
    if (bInit) {
      bInit = false;
      addPieGraphs();
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