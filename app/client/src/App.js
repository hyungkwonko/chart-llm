// App.js
import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

import Header from './components/Header';
import ChooseType from './components/ChooseType';
import VegaLiteView from './components/VegaLiteView';

function App() {
  const debugTF = true;
  // const debugTF = false;

  const colStyleLightBlue = debugTF ? { backgroundColor: 'lightblue' } : {};
  const colStylePink = debugTF ? { backgroundColor: 'pink', height: '450px' } : { height: '450px' };
  const colStyleBeige = debugTF ? { backgroundColor: 'beige', height: '450px' } : { height: '450px' };
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
        <Col xs={12} md={2} >
          <Row style={colStyleLightGreen}>
            <ChooseType
              datasetTypes={[
                { id: 'l1', label: 'L1 Caption' },
                { id: 'l2', label: 'L2 Caption' },
                { id: 'utterance', label: 'Utterance' },
                { id: 'lookup', label: 'Question (Lookup)' },
                { id: 'compositional', label: 'Question (Compositional)' },
                { id: 'openEnded', label: 'Question (Open-ended)' }
              ]}
              onTypeSelect={(selectedId) => console.log("Selected Dataset Type ID:", selectedId)}
            />
          </Row>
        </Col>
        <Col xs={12} md={6} >
          <Row style={colStyleOrange}>
            <VegaLiteView />
          </Row>
          <Row style={colStyleGreen}>
            b2
          </Row>
        </Col>
        <Col xs={12} md={4} >
          <Row style={colStylePink} >
            c1
          </Row>
          <Row style={colStyleBeige}>
            c2
          </Row>
        </Col>
      </Row>
    </Container >
  );
}

export default App;