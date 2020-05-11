import Router from '@koa/router'
import SurveyController from '../controllers/surveys'
import { authenticationRequired } from '../middlewares/protect'

const survey = new Router()

survey.param('survey', SurveyController.surveyParam)

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

export default survey
