// NLSpecificTool.js
import React, { useState } from 'react';
import { Card, Form, Button, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { useSelector, useDispatch } from 'react-redux';
import {
  updateSelectedSemantics, updateUtteranceType, updateFeature, updateConsider,
  updateQuestionType, updateVisualizationType, updateHigherLevelDecision,
  updateSelectedAxis, updateAxisScore, updateParaphrase
} from '../redux/textSlice';


function NLSpecificTool() {
  const dispatch = useDispatch();

  const initialSemantics = ['Data', 'Transform', 'Mark', 'Chart-Type', 'Encoding', 'Style', 'Interaction'];

  const [semantics, setSemantics] = useState(initialSemantics);
  const selectedSemantics = useSelector(state => state.text.selectedSemantics);

  const [newSemantic, setNewSemantic] = useState('');

  const feature = useSelector(state => state.text.feature);
  const consider = useSelector(state => state.text.consider);
  const utteranceType = useSelector(state => state.text.utteranceType);

  const questionType = useSelector(state => state.text.questionType);
  const visualizationType = useSelector(state => state.text.visualizationType);
  const higherLevelDecision = useSelector(state => state.text.higherLevelDecision);

  const paraphrase = useSelector(state => state.text.paraphrase);
  const selectedAxis = useSelector(state => state.text.selectedAxis);
  const axisScore = useSelector(state => state.text.axisScore);

  const AXES = {
    clarity: "Score 1 gives informal and used in everyday conversation, while score 5 follows established rules and conventions and is used in more formal situations.",
    expertise: "Score 1 is often used by experts in a particular field and includes specialized terminology and jargon. Score 5, on the other hand, is more accessible to a general audience and avoids the use of complex terms.",
    formality: "Score 1 expresses personal opinions, feelings, or judgments, while score 5 presents facts or information without bias or personal interpretation.",
    subjectivity: "Score 1 relies on the context, shared knowledge, and non-verbal cues to convey meaning. Score 5, on the other hand, is clear and direct. It leaves little room for interpretation or misunderstanding."
  };

  const selectedTypeId = useSelector(state => state.text.selectedTypeId);

  const handleCheckboxChange = (semantic) => {
    const updatedSemantics = {
      ...selectedSemantics,
      [semantic]: !selectedSemantics[semantic]
    };
    dispatch(updateSelectedSemantics(updatedSemantics));
  };

  const handleAddSemantic = () => {
    if (newSemantic && !semantics.includes(newSemantic)) {
      setSemantics(prev => [...prev, newSemantic]);
      setNewSemantic('');
    }
  };

  const handleRemoveSemantic = (semanticToRemove) => {
    setSemantics(prev => prev.filter(smt => smt !== semanticToRemove));
    const updatedSelectedSemantics = { ...selectedSemantics };
    delete updatedSelectedSemantics[semanticToRemove];
    dispatch(updateSelectedSemantics(updatedSelectedSemantics));
  };

  const handleFeature = (e) => {
    dispatch(updateFeature(e.target.value));
  };

  const handleConsider = (e) => {
    dispatch(updateConsider(e.target.value));
  };

  const handleUtteranceTypeChange = (e) => {
    dispatch(updateUtteranceType(e.target.value));
  };

  const handleQuestionTypeChange = (e) => {
    dispatch(updateQuestionType(e.target.value));
  };

  const handleVisualizationTypeChange = (e) => {
    dispatch(updateVisualizationType(e.target.value));
  };

  const handlehigherLevelDecision = (e) => {
    dispatch(updateHigherLevelDecision(e.target.value));
  };

  const handleParaphraseChange = () => {
    dispatch(updateParaphrase(paraphrase ? false : true));
  };

  const handleSelectedAxisChange = (e) => {
    dispatch(updateSelectedAxis(e.target.value));
  };

  const handleAxisScoreChange = (e) => {
    dispatch(updateAxisScore(e.target.value));
  };

  return (
    <>
      {selectedTypeId === 'l2' && (
        <Card style={{ border: '0px' }}>
          <Card.Body>
            <Card.Title>What is the most prominent and meaningful feature in this chart to analyze?</Card.Title>
            <Form.Control
              as="textarea"
              rows={7}
              placeholder="Enter feature details"
              value={feature}
              onChange={handleFeature}
            />
          </Card.Body>
        </Card>
      )}

      {selectedTypeId === 'utterance' && (
        <Card style={{ border: '0px' }}>
          <Card.Body>
            <Card.Title>Utterance Type</Card.Title>
            <Form.Group>
              {['command', 'query', 'question'].map(type => (
                <Form.Check
                  key={type}
                  type="radio"
                  id={`utterance-${type}`}
                  label={type.charAt(0).toUpperCase() + type.slice(1)}
                  name="utteranceType"
                  value={type}
                  checked={utteranceType === type}
                  onChange={handleUtteranceTypeChange}
                />
              ))}
            </Form.Group>
          </Card.Body>
        </Card>
      )}

      {(selectedTypeId === 'l1' || selectedTypeId === 'utterance') && (
        <Card style={{ border: '0px' }}>
          <Card.Body>
            <Card.Title>Chart Semantics</Card.Title>
            {semantics.map(semantic => (
              <div key={semantic} className="d-flex justify-content-between align-items-center my-2">
                <Form.Check
                  type="checkbox"
                  id={semantic}
                  label={semantic}
                  checked={!!selectedSemantics[semantic]}
                  onChange={() => handleCheckboxChange(semantic)}
                />
                {!initialSemantics.includes(semantic) && (
                  <Button variant="danger" size="sm" onClick={() => handleRemoveSemantic(semantic)}>Remove</Button>
                )}
              </div>
            ))}
            <div className="d-flex justify-content-between">
              <Form.Control
                type="text"
                placeholder="+ Add additional semantics"
                value={newSemantic}
                onChange={(e) => setNewSemantic(e.target.value)}
                className="me-2"
                style={{ flex: 1 }}
              />
              <Button onClick={handleAddSemantic}>Add</Button>
            </div>
          </Card.Body>
        </Card>
      )}

      {selectedTypeId === 'utterance' && (
        <>
          <Card style={{ border: '0px' }}>
            <Card.Body>
              <Card.Title>Please provide additional considerations</Card.Title>
              <Form.Control
                as="textarea"
                placeholder="Write here..."
                value={consider}
                onChange={handleConsider}
              />
            </Card.Body>
          </Card>
        </>
      )}

      {selectedTypeId === 'question' && (
        <>
          <Card style={{ border: '0px' }}>
            <Card.Body>
              <Card.Title>Choose Question Type</Card.Title>
              {['lookup', 'compositional', 'open-ended'].map(type => (
                <Form.Check
                  type="radio"
                  key={`question-type-${type}`}
                  id={`question-type-${type}`}
                  label={type.charAt(0).toUpperCase() + type.slice(1)}
                  name="questionType"
                  value={type}
                  checked={questionType === type}
                  onChange={handleQuestionTypeChange}
                />
              ))}
            </Card.Body>
          </Card>
          {(questionType === 'lookup' || questionType === 'compositional') && (
            <Card style={{ border: '0px' }}>
              <Card.Body>
                <Card.Title>Choose Visualization Type</Card.Title>
                <Form.Check
                  type="radio"
                  id="visual"
                  label="Visual"
                  name="visualizationType"
                  value="visual"
                  checked={visualizationType === 'visual'}
                  onChange={handleVisualizationTypeChange}
                />
                <Form.Check
                  type="radio"
                  id="nonvisual"
                  label="Non-Visual"
                  name="visualizationType"
                  value="nonvisual"
                  checked={visualizationType === 'nonvisual'}
                  onChange={handleVisualizationTypeChange}
                />
              </Card.Body>
            </Card>
          )}
          <Card style={{ border: '0px' }}>
            <Card.Body>
              <Card.Title>What higher-level decision can be made by analyzing this chart?</Card.Title>
              <Form.Control
                as="textarea"
                rows={4}
                placeholder="Please write a higher level decision"
                value={higherLevelDecision}
                onChange={handlehigherLevelDecision}
              />
            </Card.Body>
          </Card>
        </>
      )}

      {(selectedTypeId === 'utterance' || selectedTypeId === 'question') && (
        <Card style={{ border: '0px' }}>
          <Card.Body>
            <div className="d-flex justify-content-between align-items-center">
              <Card.Title>Paraphrase</Card.Title>
              <Form.Check
                type="switch"
                id="paraphrase-switch"
                checked={paraphrase}
                onChange={handleParaphraseChange}
              />
            </div>
            <Form.Label>1. Choose language axis for paraphrase:</Form.Label>
            {['clarity', 'expertise', 'formality', 'subjectivity'].map((axis) => (
              <OverlayTrigger
                key={axis}
                placement="top"
                overlay={
                  <Tooltip id={`tooltip-${axis}`}>
                    {AXES[axis]}
                  </Tooltip>
                }
              >
                <span className="d-inline-block" style={{ width: '100%' }}>
                  <Form.Check
                    type="radio"
                    id={axis}
                    label={axis.charAt(0).toUpperCase() + axis.slice(1)}
                    name="languageAxis"
                    value={axis}
                    checked={selectedAxis === axis}
                    disabled={!paraphrase}
                    onChange={handleSelectedAxisChange}
                  />
                </span>
              </OverlayTrigger>
            ))}
            <Form.Label>2. Choose score for {selectedAxis.charAt(0).toUpperCase() + selectedAxis.slice(1)}: {axisScore}</Form.Label>
            <Form.Range
              type="range"
              min="1"
              max="5"
              value={axisScore}
              disabled={!paraphrase}
              onChange={handleAxisScoreChange}
              className="custom-range-slider"
            />
          </Card.Body>
        </Card>
      )}
    </>
  );
}

export default NLSpecificTool;
