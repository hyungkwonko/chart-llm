// ChooseType.js
import React from 'react';
import { Card, Button, Container, Form } from 'react-bootstrap';
import { useSelector, useDispatch } from 'react-redux';
import { updateSelectedTypeId, updateChartIndex, updateIndex, updateNL, setLoading } from '../redux/textSlice';


function ChooseType({ datasetTypes }) {
  const dispatch = useDispatch();
  const chartIndex = useSelector((state) => state.text.chartIndex);
  const selectedTypeId = useSelector((state) => state.text.selectedTypeId);
  const selectedIndices = useSelector((state) => state.text.selectedIndices);

  const pageType = useSelector(state => state.text.pageType);

  // Task 1-1, 2
  const selectedSemantics = useSelector(state => state.text.selectedSemantics);

  // Task 1-2
  const feature = useSelector(state => state.text.feature);

  // Task 2
  const utteranceType = useSelector(state => state.text.utteranceType);
  const consider = useSelector(state => state.text.consider);

  // Task 3
  const questionType = useSelector(state => state.text.questionType);
  const visualizationType = useSelector(state => state.text.visualizationType);
  const higherLevelDecision = useSelector(state => state.text.higherLevelDecision);

  // Task 4
  const paraphrase = useSelector(state => state.text.paraphrase);
  const selectedAxis = useSelector(state => state.text.selectedAxis);
  const axisScore = useSelector(state => state.text.axisScore);

  const isLoading = useSelector((state) => state.text.isLoading);

  const handleTypeSelect = (typeId) => {
    dispatch(updateSelectedTypeId(typeId));
  };

  const handleCardClick = (index) => {
    dispatch(updateChartIndex(index));
  };

  const handleCheckboxChange = (index) => {
    dispatch(updateIndex(index));
  };

  const handleSelectAllChange = (event) => {
    if (event.target.checked) {
      dispatch(updateIndex([...Array(10).keys()]));
    } else {
      dispatch(updateIndex([]));
    }
  };

  const handleSubmit = async () => {
    dispatch(setLoading(true));

    const data = {
      pageType,
      selectedTypeId,
      selectedIndices,
      selectedSemantics,
      feature,
      consider,
      utteranceType,
      questionType,
      visualizationType,
      higherLevelDecision,
      paraphrase,
      selectedAxis,
      axisScore
    };

    try {
      // const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/generate_nl`, {
      const response = await fetch('/generate_nl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Response from backend:', result);
      dispatch(updateNL(result['nl']));
    } catch (error) {
      console.error('Error sending data to backend:', error);
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <Container>
      {datasetTypes.map(({ id, label }) => (
        <Card
          key={id}
          className='mb-4'
          style={{
            height: "70px",
            cursor: 'pointer',
            backgroundColor: id === selectedTypeId ? 'whitesmoke' : 'transparent',
          }}
          onClick={() => handleTypeSelect(id)}
        >
          <Card.Body className="d-flex justify-content-between align-items-center">
            <div>
              <p className='bold-text my-0'>{label}</p>
            </div>
            <Button
              onClick={(e) => { e.stopPropagation() }}
              className='circle-button'
              variant={id === selectedTypeId ? 'dark' : 'outline-dark'}
            >
            </Button>
          </Card.Body>
        </Card>
      ))}

      {[...Array(10).keys()].map(index => (
        <div key={index} className="d-flex justify-content-between align-items-center mb-2">
          <Card
            className="flex-grow-1 py-1"
            style={{
              fontSize: "14px",
              cursor: 'pointer',
              backgroundColor: chartIndex === index ? 'lightgrey' : 'transparent',
              border: '0px',
              marginRight: '10px'
            }}
            onClick={() => handleCardClick(index)}
          >
            <span style={{ marginLeft: '5px' }}>Chart {index}</span>
          </Card>
          <Form.Check
            type="checkbox"
            id={`checkbox-${index}`}
            checked={selectedIndices.includes(index)}
            onChange={() => handleCheckboxChange(index)}
          />
        </div>
      ))}

      <div className="d-flex justify-content-between align-items-center mb-2">
        <Card
          className="flex-grow-1 py-2"
          style={{
            fontSize: "14px",
            border: '0px',
            marginRight: '10px'
          }}
        >
          <span style={{ marginLeft: '5px' }}>Select All Charts</span>
        </Card>
        <Form.Check
          type="checkbox"
          id="select-all-checkbox"
          checked={selectedIndices.length === 10}
          onChange={handleSelectAllChange}
        />
      </div>

      <div className="d-flex align-items-center gap-2 mt-2">
        <Button
          variant="outline-danger"
          size="sm"
          className='w-100'
          disabled={
            selectedIndices.length === 0 ||
            (['l1'].includes(selectedTypeId) && !Object.values(selectedSemantics).some(value => value)) ||
            (['l2'].includes(selectedTypeId) && feature === '') ||
            (['question'].includes(selectedTypeId) && higherLevelDecision === '') ||
            isLoading
          }
          onClick={handleSubmit}
        >
          Generate NL
        </Button>
      </div>
    </Container>
  );
}

export default ChooseType;
