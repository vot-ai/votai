import Router from '@koa/router'
import SurveyController from '../controllers/surveys'
import { authenticationRequired } from '../middlewares/protect'

const survey = new Router()

survey.param('survey', SurveyController.surveyParam)

survey.post('/', authenticationRequired(), SurveyController.create)

survey.get('/:survey', SurveyController.get)
survey.post('/:survey/access', SurveyController.requestAccess)

export default survey
