// textSlice.js
import { createSlice } from '@reduxjs/toolkit';

export const textSlice = createSlice({
  name: 'text',
  initialState: {
    value: '',
    pageType: 'c0',
    selectedTypeId: 'utterance',
    chartIndex: 0,
    selectedIndices: [],
    selectedSemantics: {},
    nl: {},
    isLoading: false,
    feature: '',
    consider: '',
    utteranceType: 'command',
    questionType: 'lookup',
    visualizationType: 'visual',
    higherLevelDecision: '',
    paraphrase: false,
    selectedAxis: 'clarity',
    axisScore: 3,
  },
  reducers: {
    updateText: (state, action) => {
      state.value = action.payload;
    },
    updatePageType: (state, action) => {
      state.pageType = action.payload;
    },
    updateSelectedTypeId: (state, action) => {
      state.selectedTypeId = action.payload;
    },
    updateChartIndex: (state, action) => {
      state.chartIndex = action.payload;
    },
    updateIndex: (state, action) => {
      if (Array.isArray(action.payload)) {
        state.selectedIndices = action.payload;
      } else {
        const index = action.payload;
        const currentIndex = state.selectedIndices.indexOf(index);
        if (currentIndex === -1) {
          state.selectedIndices.push(index);
        } else {
          state.selectedIndices.splice(currentIndex, 1);
        }
      }
    },
    updateSelectedSemantics: (state, action) => {
      state.selectedSemantics = action.payload;
    },
    updateNL: (state, action) => {
      state.nl = action.payload;
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    updateConsider: (state, action) => {
      state.consider = action.payload;
    },
    updateFeature: (state, action) => {
      state.feature = action.payload;
    },
    updateUtteranceType: (state, action) => {
      state.utteranceType = action.payload;
    },
    updateQuestionType: (state, action) => {
      state.questionType = action.payload;
    },
    updateVisualizationType: (state, action) => {
      state.visualizationType = action.payload;
    },
    updateHigherLevelDecision: (state, action) => {
      state.higherLevelDecision = action.payload;
    },
    updateParaphrase: (state, action) => {
      state.paraphrase = action.payload;
    },
    updateSelectedAxis: (state, action) => {
      state.selectedAxis = action.payload;
    },
    updateAxisScore: (state, action) => {
      state.axisScore = action.payload;
    },
  },
});

export const { updateText, updatePageType, updateSelectedTypeId, updateChartIndex, updateIndex,
  updateSelectedSemantics, updateNL, setLoading, updateUtteranceType, updateFeature, updateConsider,
  updateQuestionType, updateVisualizationType, updateHigherLevelDecision,
  updateParaphrase, updateSelectedAxis, updateAxisScore } = textSlice.actions;

export default textSlice.reducer;
