// App.js
import React from 'react';
import { useSelector } from 'react-redux';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

import WelcomePage from './components/WelcomePage';
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

  const pageType = useSelector((state) => state.text.pageType);

  return (
    <>
      {pageType === 'c0' && (
        <WelcomePage />
      )}
      {(pageType === 'c1' || pageType === 'c2') && (
        <Container>
          <Row>
            <Col style={colStyleLightBlue}>
              <Header />
            </Col>
          </Row>
          {pageType === 'c1' && (
            <Row>
              <Col xs={12} md={10} >
                <Row style={colStyleOrange}>
                  <VegaLiteView />
                </Row>
                <Row style={colStyleGreen}>
                  <ResultView />
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
          )}
          {pageType === 'c2' && (
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
          )}
        </Container>
      )}
    </>
  )
}

export default App;