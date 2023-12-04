// App.js
import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

import Header from './components/Header';
import ChooseType from './components/ChooseType';
import VegaLiteView from './components/VegaLiteView';
import ResultView from './components/ResultView';
import NLSpecificTool from './components/NLSpecificTool';

function App() {
  // const debugTF = true;
  const debugTF = false;

  const colStyleLightBlue = debugTF ? { backgroundColor: 'lightblue' } : {};
  const colStylePink = debugTF ? { backgroundColor: 'pink', height: '900px' } : { height: '900px' };
  const colStyleLightGreen = debugTF ? { backgroundColor: 'lightgreen', height: '900px' } : { height: '900px' };
  const colStyleOrange = debugTF ? { backgroundColor: 'orange', height: '450px' } : { height: '450px' };
  const colStyleGreen = debugTF ? { backgroundColor: 'green', height: '450px' } : { height: '450px' };

  return (
    <Container>
      <Row>
        <Col style={colStyleLightBlue}>
          <Header />
        </Col>
      </Row>
      <Row>
        <Col xs={12} md={6} >
          <Row style={colStyleOrange}>
            <VegaLiteView />
          </Row>
          <Row style={colStyleGreen}>
            <ResultView />
          </Row>
        </Col>
        <Col xs={12} md={4} >
          <Row style={colStylePink} >
            <NLSpecificTool />
          </Row>
        </Col>
        <Col xs={12} md={2} >
          <Row style={colStyleLightGreen}>
            <ChooseType
              datasetTypes={[
                { id: 'l1', label: 'L1 Caption' },
                { id: 'l2', label: 'L2 Caption' },
                { id: 'utterance', label: 'Utterance' },
                { id: 'question', label: 'Question' },
              ]}
            />
          </Row>
        </Col>
      </Row>
    </Container >
  );
}

export default App;