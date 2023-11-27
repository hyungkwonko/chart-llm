// ChooseType.js
import React, { useState } from 'react';
import { Card, Button, Container } from 'react-bootstrap';

function ChooseType({ datasetTypes, onTypeSelect }) {
  const [selectedTypeId, setSelectedTypeId] = useState(null);

  const handleTypeSelect = (typeId) => {
    setSelectedTypeId(typeId);
    onTypeSelect(typeId);
  };

  return (
    <Container>
      {datasetTypes.map(({ id, label }) => (
        <Card
          key={id}
          className='my-2'
          style={{
            height: "70px",
            border: "0px",
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
              onClick={(e) => {
                e.stopPropagation();
              }}
              className='circle-button'
              variant={id === selectedTypeId ? 'dark' : 'outline-dark'}
            >
            </Button>
          </Card.Body>
        </Card>
      ))}
    </Container>
  );
}

export default ChooseType;
