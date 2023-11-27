import { configureStore } from '@reduxjs/toolkit'
import textSlice from './textSlice'

export default configureStore({
  reducer: {
    textSlice: textSlice,
  },
})