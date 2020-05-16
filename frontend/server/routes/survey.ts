import Router from '@koa/router'
import SurveyController from '../controllers/surveys'
import AnnotatorController from '../controllers/annotators'
import { authenticationRequired } from '../middlewares/protect'
import { hasSurveyAccess } from '../middlewares/survey'
import { userIsAnnotator } from '../middlewares/annotator'

const survey = new Router()
const annotator = new Router()

// Annotator endpoints
annotator.get('/', AnnotatorController.getAnnotator)
annotator.post('/vote', userIsAnnotator(), AnnotatorController.vote)
annotator.post('/skip', userIsAnnotator(), AnnotatorController.skip)

// Add survey param loader
survey.param('survey', SurveyController.surveyParam)

// Survey endpoints
survey.post('/', authenticationRequired(), SurveyController.create)
survey.get('/my', SurveyController.listUserOwned)
survey.get('/annotated', SurveyController.listFromAnnotator)
survey.get('/:survey', SurveyController.get)
survey.patch('/:survey', authenticationRequired(), SurveyController.update)
survey.delete('/:survey', authenticationRequired(), SurveyController.delete)
survey.post('/:survey/access', SurveyController.requestAccess)
survey.post(
  '/:survey/change-password',
  authenticationRequired(),
  SurveyController.changePassword
)

// Register annotator endpoints
survey.use(
  '/:survey/annotator',
  authenticationRequired(),
  hasSurveyAccess(),
  annotator.routes(),
  annotator.allowedMethods()
)

export default survey
