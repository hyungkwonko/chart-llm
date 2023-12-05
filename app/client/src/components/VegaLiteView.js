// VegaLiteView.js
import React, { useEffect, useRef } from 'react';
import vegaEmbed from 'vega-embed';
import { useSelector } from 'react-redux';

function VegaLiteView() {
  const vegaChartRef = useRef();
  const chartIndex = useSelector((state) => state.text.chartIndex);

  useEffect(() => {
    const loadVegaLiteChart = () => {
      // fetch(`${process.env.REACT_APP_BACKEND_URL}/data/chart/${chartIndex}.vl.json`)
      fetch(`/data/chart/${chartIndex}.vl.json`)
        .then(response => response.json())
        .then(spec => {
          vegaEmbed(vegaChartRef.current, spec)
            .then((res) => console.log(res))
            .catch(err => console.error(err));
        })
        .catch(error => console.error('Error fetching Vega-Lite spec:', error));
    };

    loadVegaLiteChart();
  }, [chartIndex]);

  return (
    <div ref={vegaChartRef} style={{ width: "100%", height: "100%" }}></div>
  );
}

export default VegaLiteView;