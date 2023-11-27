// VegaLiteView.js
import React, { useRef } from 'react';
import { Button } from 'react-bootstrap';
import vegaEmbed from 'vega-embed';


function VegaLiteView() {

  const vegaChartRef = useRef();

  const fetchVegaLiteSpec = () => {
    fetch('http://localhost:5678/data/chart/CHL.vl.json')
      .then(response => response.json())
      .then(spec => {
        vegaEmbed(vegaChartRef.current, spec)
          .then((res) => console.log(res))
          .catch(err => console.error(err));
      })
      .catch(error => console.error('Error fetching Vega-Lite spec:', error));
  };

  return (
    <>
      <div ref={vegaChartRef} style={{ width: "100%", height: "90%" }}></div>
      <div className="d-flex justify-content-between align-items-center w-100">
        <div className="d-flex align-items-center gap-2">
          <Button className='circle-button2'
            variant="outline-dark"
            size="sm"
          // onClick={() => changeTestIndex(-1)}
          // disabled={testIndex <= 0}
          >
            {"<"}
          </Button>
          <h4 className='my-0'>Chart index</h4>
          <Button className='circle-button2'
            variant="outline-dark"
            size="sm"
          // onClick={() => changeTestIndex(+1)}
          // disabled={testIndex > 3}
          >
            {">"}
          </Button>
        </div>
        <div className="d-flex align-items-center gap-2">
          <Button variant="outline-dark" size="sm"
          // onClick={() => updateTest(false)}
          >
            Run
          </Button>
          <Button variant="outline-dark" size="sm"
          // onClick={runTest}
          >
            Run All
          </Button>
          <Button variant="outline-dark" size="sm" onClick={fetchVegaLiteSpec}>
            Load Chart
          </Button>
        </div>
      </div>
    </>
  );
}

export default VegaLiteView;
