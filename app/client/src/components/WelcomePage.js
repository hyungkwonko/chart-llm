// WelcomePage.js
import React, { useRef, useState, useEffect } from 'react';
import vegaEmbed from 'vega-embed';
import { Container, Row, Col, Button, Card, Form } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import { updatePageType } from '../redux/textSlice';


const WelcomePage = () => {
  const vegaChartRef1 = useRef();
  const vegaChartRef2 = useRef();

  const [formalityScore, setFormalityScore] = useState(1);
  const [isVisible, setIsVisible] = useState(false);

  const dispatch = useDispatch();

  const handlePageTypeChange = (newPageType) => {
    dispatch(updatePageType(newPageType));
  };

  const loadVegaLiteChart = (chartRef) => {
    // fetch(`${process.env.REACT_APP_BACKEND_URL}/data/chart/sample.vl.json`)
    fetch('/data/chart/sample.vl.json')
      .then(response => response.json())
      .then(spec => {
        vegaEmbed(chartRef.current, spec)
          .then((res) => console.log(res))
          .catch(err => console.error(err));
      })
      .catch(error => console.error('Error fetching Vega-Lite spec:', error));
  };

  useEffect(() => {
    loadVegaLiteChart(vegaChartRef1);
    loadVegaLiteChart(vegaChartRef2);
  }, []);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const sentences = {
    1: "Can you put together a bar chart showing the aggregate profit from various geographical areas?",
    2: "Could you create a bar chart that illustrates the aggregate profit from various geographical areas?",
    3: "Please create a bar chart illustrating the aggregate profit from various geographical areas.",
    4: "It is requested that you create a bar chart illustrating the aggregate profit from various geographical areas.",
    5: "You are required to construct a bar chart illustrating the aggregate profit from various geographical areas."
  };

  return (
    <Container className="my-4 w-50">
      <Row className="justify-content-center my-4">
        <h1 className="text-center mb-2">VL2NL Framework Application</h1>
        <Card className="mb-2" style={{ border: '0px' }}>
          <Card.Body>
            <Card.Title className="text-danger">What is VL2NL (Vega-Lite to Natural Language) Framework?</Card.Title>
            <Card.Text>
              It is a framework to generate NL datasets like L1/L2 captions, utterances, questions using Vega-Lite specifications and LLMs. Our framework can accurately simulate semantics of each NL dataset. It also provides score-based paraphrase to increase the syntactic diversity of NL datasets.
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>

      <Row className="justify-content-center my-4">
        <Card>
          <h3 className="text-center my-4">NL datasets Generation</h3>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div ref={vegaChartRef1} style={{ width: '80%' }}></div>
            <div style={{ marginRight: '50px', fontSize: '50px' }}>→</div>
            <div>
              NL Dataset: 1) Create a bar chart showing the sum of profit from different regions. 2) ...
            </div>
          </div>

          <Card.Body>
            <Card.Title className="mt-3">Utterance</Card.Title>
            <Card.Text>
              An utterance is what a user would say to generate a given chart. There are three types of utterances.
            </Card.Text>
            <Card.Text>
              1. <b>Command type:</b> requires a single value retrieval.
            </Card.Text>
            <p style={{ fontStyle: 'italic' }}>e.g., Create a bar chart showing the sum of profit from different regions.</p>
            <Card.Text>
              2. <b>Query type:</b> is similar to SQL query.
            </Card.Text>
            <p style={{ fontStyle: 'italic' }}>e.g., Region by Sum(Profit)</p>
            <Card.Text>
              3. <b>Question type:</b> is a question about making the chart.
            </Card.Text>
            <p style={{ fontStyle: 'italic' }}>e.g., Can you generate a chart to show profits in different regions?</p>

            <div className="d-flex justify-content-center">
              <Button variant="outline-secondary" onClick={toggleVisibility}>
                {isVisible ? 'Hide' : 'Show'} other types of NL datasets
              </Button>
            </div>

            {isVisible && (
              <>
                <Card.Title className="mt-3">L1 Caption</Card.Title>
                <Card.Text>
                  It contains elemental and encoded properties of the visualization (i.e., the visual components that comprise a graphical representation's design and construction).
                </Card.Text>
                <Card.Text style={{ fontStyle: 'italic' }}>
                  e.g., This is a bar chart that uses data from a superstore. The chart encodes the 'Region' field on the x-axis and the sum of 'Profit' on the y-axis. The 'Ship Status' field is represented by different colors.
                </Card.Text>

                <Card.Title className="mt-3">L2 caption</Card.Title>
                <Card.Text>
                  It contains statistical and relational properties of the visualization.
                </Card.Text>
                <Card.Text style={{ fontStyle: 'italic' }}>
                  e.g., The visualization presents the total profit for each region, with the West region having the highest profit of approximately 67860.56 and the South region having the lowest profit of approximately 26551.72.
                </Card.Text>

                <Card.Title className="mt-3">Question</Card.Title>
                <Card.Text>
                  Questions are used to analyze charts and elicit high-level decision. There are different types of questions.
                </Card.Text>

                <Card.Text>
                  1. <b>A lookup question</b> requires a single value retrieval.
                </Card.Text>
                <p style={{ fontStyle: 'italic' }}>e.g., What is the Sum(profit) of Central region?</p>

                <Card.Text>
                  2. <b>A compositional question</b> requires multiple operations
                </Card.Text>
                <p style={{ fontStyle: 'italic' }}>e.g., What is the average of Sum(profit) for Shipped early?</p>

                <Card.Text>
                  3. <b>A visual question</b> includes visual attributes such as color, length, size, or position.
                </Card.Text>
                <p style={{ fontStyle: 'italic' }}>e.g., Which region has the longest bar representing the highest total profit?</p>

                <Card.Text>
                  4. <b>A non-visual question</b> does not include any visual attributes such as color, length, size, or position.
                </Card.Text>

                <Card.Text>
                  5. <b>An open-ended question</b> encourages deeper reflection on the underlying reasons or causes behind specific events or patterns.
                </Card.Text>
                <p style={{ fontStyle: 'italic' }}>e.g., What is the reason for this pattern?</p>
              </>
            )}
          </Card.Body>
        </Card>
      </Row>


      <Row className="justify-content-center my-4">
        <Card>
          <h3 className="text-center mt-4">Score-based Paraphrase</h3>
          <Card.Body>
            <Card.Text>
              The framework can paraphrase NL datasets using four language axes:<br />
              - Clarity (implicit -- explicit)<br />
              - Expertise (non-technical -- technical)<br />
              - Formality (colloquial -- standard)<br />
              - Subjectivity (subjective -- objective)
            </Card.Text>
            <Card.Title className="mt-3">Original Sentence</Card.Title>
            <Card.Text style={{ fontStyle: 'italic' }}>
              e.g., Create a bar chart showing the sum of profit from different regions.
            </Card.Text>
            <Card.Title className="mt-3">Paraphrased Sentence (Formality score: {formalityScore})</Card.Title>
            <Card.Text style={{ fontStyle: 'italic' }}>
              &gt; {sentences[formalityScore]}
            </Card.Text>
            <Row>
              <Col xs={6} className="text-start">
                <Card.Text style={{ fontStyle: 'italic' }}>
                  Score 1: Colloquial
                </Card.Text>
              </Col>
              <Col xs={6} className="text-end">
                <Card.Text style={{ fontStyle: 'italic' }}>
                  Score 5: Standard
                </Card.Text>
              </Col>
            </Row>
            <Form.Range
              type="range"
              min="1"
              max="5"
              value={formalityScore}
              onChange={e => setFormalityScore(Number(e.target.value))}
              className="form-range"
            />
          </Card.Body>
        </Card>
      </Row>

      <Row className="justify-content-center my-3">
        <Card>
          <h3 className="text-center my-4">Task: Generating Utterances</h3>
          <Card.Body>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <div>
                NL Dataset: 1) Create a bar chart showing the sum of profit from different regions. 2) ...
              </div>
              <div style={{ marginRight: '50px', fontSize: '50px' }}>→</div>
              <div ref={vegaChartRef2} style={{ width: '80%' }}></div>
            </div>

            <Card.Text>
              You will be given Vega-Lite specifications for the stock prices of 10 tech companies. It is important to increase the semantic / syntactic diversity of the NL datasets in training AI models. Your task is to create diverse "Utterances" under two conditions. These utterances will be used to develop AI models to make chart.
            </Card.Text>

            <Card.Title className="mt-3">Condition 1: Fully-automatic</Card.Title>
            <Card.Text style={{ fontStyle: 'italic' }}>
              Generate utterances in a fully-automatic setting.
            </Card.Text>

            <Card.Title className="mt-3">Condition 2: Mixed-initiative</Card.Title>
            <Card.Text style={{ fontStyle: 'italic' }}>
              Generate utterances in a mixed-initiative setting.
            </Card.Text>
          </Card.Body>

          <h3 className="text-center mt-4">Procedure</h3>
          <Card.Body>
            <Card.Title className="my-3">Total Time: 40 minutes</Card.Title>
            <Card.Text style={{ fontStyle: 'italic' }}>
              (15 minutes) Understanding the VL2NL Framework
            </Card.Text>
            <Card.Text style={{ fontStyle: 'italic' }}>
              (15 minutes) Perform Task: Generating utterances with two conditions
            </Card.Text>
            <Card.Text style={{ fontStyle: 'italic' }}>
              (10 minutes) Post interview
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>

      <Row className="justify-content-center mt-2">
        <Col xs="auto">
          <Button variant="primary" onClick={() => handlePageTypeChange('c1')}>
            I understood the concept of VL2NL framework and interview procedure.
          </Button>
        </Col>
      </Row>
    </Container >
  );
};

export default WelcomePage;
