from collections import namedtuple

from enum import Enum

from .constants import *

MainCategories = namedtuple('MainCategories', ['id', 'key', 'version'])
MainTags = namedtuple('MainTags', ['id', 'key', 'version'])


class Categories(Enum):
    SECTORS = MainCategories(id=1, key='sectors', version=SECTOR_VERSION)
    ONE_D_MATRIX = MainCategories(id=2, key='subpillars_1d', version=SUBPILLARS_1D_VERSION)
    TWO_D_MATRIX = MainCategories(id=3, key='subpillars_2d', version=SUBPILLARS_2D_VERSION)
    SPECIFIC_NEEDS_GROUPS = MainCategories(id=4, key='specific_needs_groups', version=SPECIFIC_NEEDS_GROUP_VERSION)
    GENDER = MainCategories(id=5, key='gender', version=GENDER_VERSION)
    AGE = MainCategories(id=6, key='age', version=AGE_VERSION)
    SEVERITY = MainCategories(id=7, key='severity', version=SEVERITY_VERSION)

    @classmethod
    def all_models(cls):
        return [
            Categories.SECTORS.value._asdict(),
            Categories.ONE_D_MATRIX.value._asdict(),
            Categories.TWO_D_MATRIX.value._asdict(),
            Categories.SPECIFIC_NEEDS_GROUPS.value._asdict(),
            Categories.GENDER.value._asdict(),
            Categories.AGE.value._asdict(),
            Categories.SEVERITY.value._asdict()
        ]


class Tags(Enum):
    # Sectors Enum
    AGRICULTURE = MainTags(id=101, key='Agriculture', version=SECTOR_VERSION)
    CROSS = MainTags(id=102, key='Cross', version=SECTOR_VERSION)
    EDUCATION = MainTags(id=103, key='Education', version=SECTOR_VERSION)
    FOOD_SECURITY = MainTags(id=104, key='Food Security', version=SECTOR_VERSION)
    HEALTH = MainTags(id=105, key='Health', version=SECTOR_VERSION)
    LIVELIHOODS = MainTags(id=106, key='Livelihoods', version=SECTOR_VERSION)
    LOGISTICS = MainTags(id=107, key='Logistics', version=SECTOR_VERSION)
    NUTRITION = MainTags(id=108, key='Nutrition', version=SECTOR_VERSION)
    PROTECTION = MainTags(id=109, key='Protection', version=SECTOR_VERSION)
    SHELTER = MainTags(id=110, key='Shelter', version=SECTOR_VERSION)
    WASH = MainTags(id=111, key='WASH', version=SECTOR_VERSION)

    # 1D SubPillars
    CONTEXT_ENVIRONMENT = MainTags(id=201, key='Context->Environment', version=SUBPILLARS_1D_VERSION)
    CONTEXT_SOCIO_CULTURAL = MainTags(id=202, key='Context->Socio Cultural', version=SUBPILLARS_1D_VERSION)
    CONTEXT_ECONOMY = MainTags(id=203, key='Context->Economy', version=SUBPILLARS_1D_VERSION)
    CONTEXT_DEMOGRAPHY = MainTags(id=204, key='Context->Demography', version=SUBPILLARS_1D_VERSION)
    CONTEXT_LEGAL_AND_POLICY = MainTags(id=205, key='Context->Legal & Policy', version=SUBPILLARS_1D_VERSION)
    CONTEXT_SECURITY_AND_STABILITY = MainTags(id=206, key='Context->Security & Stability', version=SUBPILLARS_1D_VERSION)
    CONTEXT_POLITICS = MainTags(id=207, key='Context->Politics', version=SUBPILLARS_1D_VERSION)
    SHOCK_EVENT_TYPE_AND_CHARACTERISTICS = MainTags(id=208, key='Shock/Event->Type And Characteristics', version=SUBPILLARS_1D_VERSION)
    SHOCK_EVENT_UNDERLYING_AGGRAVATING_FACTORS = MainTags(id=209, key='Shock/Event->Underlying/Aggravating Factors', version=SUBPILLARS_1D_VERSION)
    SHOCK_EVENT_HAZARD_THREATS = MainTags(id=210, key='Shock/Event->Hazard & Threats', version=SUBPILLARS_1D_VERSION)
    # Key duplicated in sub piller
    # DISPLACEMENT_TYPE_NUMBERS_MOVEMENTS = 211, _('Displacement->Type/Numbers/Movements')
    DISPLACEMENT_TYPE_NUMBERS_MOVEMENTS = MainTags(id=212, key='Displacement->Type/Numbers/Movements', version=SUBPILLARS_1D_VERSION)
    DISPLACEMENT_PUSH_FACTORS = MainTags(id=213, key='Displacement->Push Factors', version=SUBPILLARS_1D_VERSION)
    DISPLACEMENT_PULL_FACTORS = MainTags(id=214, key='Displacement->Pull Factors', version=SUBPILLARS_1D_VERSION)
    DISPLACEMENT_INTENTIONS = MainTags(id=215, key='Displacement->Intentions', version=SUBPILLARS_1D_VERSION)
    DISPLACEMENT_LOCAL_INTEGRATION = MainTags(id=216, key='Displacement->Local Integration', version=SUBPILLARS_1D_VERSION)
    CASUALTIES_INJURED = MainTags(id=217, key='Casualties->Injured', version=SUBPILLARS_1D_VERSION)
    CASUALTIES_MISSING = MainTags(id=218, key='Casualties->Missing', version=SUBPILLARS_1D_VERSION)
    CASUALTIES_DEAD = MainTags(id=219, key='Casualties->Dead', version=SUBPILLARS_1D_VERSION)
    HUMANITARIAN_ACCESS_RELIEF_TO_POPULATION = MainTags(id=220, key='Humanitarian Access->Relief To Population', version=SUBPILLARS_1D_VERSION)
    HUMANITARIAN_ACCESS_POPULATION_TO_RELIEF = MainTags(id=221, key='Humanitarian Access->Population To Relief', version=SUBPILLARS_1D_VERSION)
    HUMANITARIAN_ACCESS_PHYSICAL_CONSTRAINTS = MainTags(id=222, key='Humanitarian Access->Physical Constraints', version=SUBPILLARS_1D_VERSION)
    HUMANITARIAN_ACCESS_GAPS = MainTags(id=223, key='Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps', version=SUBPILLARS_1D_VERSION)
    INFORMATION_AND_COMMUNICATION_MEANS_AND_PREFERENCES = MainTags(id=224, key='Information And Communication->Communication Means And Preferences', version=SUBPILLARS_1D_VERSION)
    INFORMATION_AND_COMMUNICATION_INFO_CHALLENGES_AND_BARRIERS = MainTags(id=225, key='Information And Communication->Information Challenges And Barriers', version=SUBPILLARS_1D_VERSION)
    INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_POP = MainTags(id=226, key='Information And Communication->Knowledge And Info Gaps (Pop)', version=SUBPILLARS_1D_VERSION)
    INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_HUM = MainTags(id=227, key='Information And Communication->Knowledge And Info Gaps (Hum)', version=SUBPILLARS_1D_VERSION)
    COVID_19_CASES = MainTags(id=228, key='Covid-19->Cases', version=SUBPILLARS_1D_VERSION)
    COVID_19_CONTACT_CASES = MainTags(id=229, key='Covid-19->Contact Tracing', version=SUBPILLARS_1D_VERSION)
    COVID_19_DEATHS = MainTags(id=230, key='Covid-19->Deaths', version=SUBPILLARS_1D_VERSION)
    COVID_19_HOSPITALIZATION_AND_CARE = MainTags(id=231, key='Covid-19->Hospitalization & Care', version=SUBPILLARS_1D_VERSION)
    COVID_19_RESTRICTION_MEASURES = MainTags(id=232, key='Covid-19->Restriction Measures', version=SUBPILLARS_1D_VERSION)
    COVID_19_TESTING = MainTags(id=233, key='Covid-19->Testing', version=SUBPILLARS_1D_VERSION)
    COVID_19_VACCINATION = MainTags(id=234, key='Covid-19->Vaccination', version=SUBPILLARS_1D_VERSION)

    # 2D SubPillars
    AT_RISK_NUMBER_OF_PEOPLE = MainTags(id=301, key='At Risk->Number Of People At Risk', version=SUBPILLARS_2D_VERSION)
    AT_RISK_VULNERABILITIES = MainTags(id=302, key='At Risk->Risk And Vulnerabilities', version=SUBPILLARS_2D_VERSION)
    CAPACITIES_RESPONSE_INTERNATIONAL = MainTags(id=303, key='Capacities & Response->International Response', version=SUBPILLARS_2D_VERSION)
    CAPACITIES_RESPONSE_LOCAL = MainTags(id=304, key='Capacities & Response->Local Response', version=SUBPILLARS_2D_VERSION)
    CAPACITIES_RESPONSE_NATIONAL = MainTags(id=305, key='Capacities & Response->National Response', version=SUBPILLARS_2D_VERSION)
    CAPACITIES_RESPONSE_NUM_PEOPLE_REACHED = MainTags(id=306, key='Capacities & Response->Number Of People Reached/Response Gaps', version=SUBPILLARS_2D_VERSION)
    HUMANITARIAN_CONDITIONS_COPING_MECHANISMS = MainTags(id=307, key='Humanitarian Conditions->Coping Mechanisms', version=SUBPILLARS_2D_VERSION)
    HUMANITARIAN_CONDITIONS_LIVING_STANDARDS = MainTags(id=308, key='Humanitarian Conditions->Living Standards', version=SUBPILLARS_2D_VERSION)
    HUMANITARIAN_CONDITIONS_NUM_PEOPLE_IN_NEED= MainTags(id=309, key='Humanitarian Conditions->Number Of People In Need', version=SUBPILLARS_2D_VERSION)
    HUMANITARIAN_CONDITIONS_PHY_MENTAL_WELL_BEING = MainTags(id=310, key='Humanitarian Conditions->Physical And Mental Well Being', version=SUBPILLARS_2D_VERSION)
    IMPACT_DRIVER_AGGRAVATING_FACTORS = MainTags(id=311, key='Impact->Driver/Aggravating Factors', version=SUBPILLARS_2D_VERSION)
    IMPACT_ON_PEOPLE = MainTags(id=312, key='Impact->Impact On People', version=SUBPILLARS_2D_VERSION)
    IMPACT_ON_SYSTEMS_SRV_NET = MainTags(id=313, key='Impact->Impact On Systems, Services And Networks', version=SUBPILLARS_2D_VERSION)
    IMPACT_NUM_OF_PEOPLE_AFFECTED = MainTags(id=314, key='Impact->Number Of People Affected', version=SUBPILLARS_2D_VERSION)
    PRIORITY_INTERVENTIONS_HUMANITARIAN_STAFF = MainTags(id=315, key='Priority Interventions->Expressed By Humanitarian Staff', version=SUBPILLARS_2D_VERSION)
    PRIORITY_INTERVENTIONS_EXPRESSED_BY_POPULATION = MainTags(id=316, key='Priority Interventions->Expressed By Population', version=SUBPILLARS_2D_VERSION)
    PRIORITY_NEEDS_EXPRESSED_BY_HUMANITARIAN_STAFF = MainTags(id=317, key='Priority Needs->Expressed By Humanitarian Staff', version=SUBPILLARS_2D_VERSION)
    PRIORITY_NEEDS_EXPRESSED_BY_POPULATION = MainTags(id=318, key='Priority Needs->Expressed By Population', version=SUBPILLARS_2D_VERSION)

    # Specific Needs Group
    CHILD_HEAD_OF_HOUSEHOLD = MainTags(id=401, key='Child Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    CHRONICALLY_ILL = MainTags(id=402, key='Chronically Ill', version=SPECIFIC_NEEDS_GROUP_VERSION)
    ELDERLY_HEAD_OF_HOUSEHOLD = MainTags(id=403, key='Elderly Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    FEMALE_HEAD_OF_HOUSEHOLD = MainTags(id=404, key='Female Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    GBV_SURVIVORS = MainTags(id=405, key='GBV survivors', version=SPECIFIC_NEEDS_GROUP_VERSION)
    INDIGENOUS_PEOPLE = MainTags(id=406, key='Indigenous people', version=SPECIFIC_NEEDS_GROUP_VERSION)
    LGBTQI = MainTags(id=407, key='LGBTQI+', version=SPECIFIC_NEEDS_GROUP_VERSION)
    MINORITIES = MainTags(id=408, key='Minorities', version=SPECIFIC_NEEDS_GROUP_VERSION)
    PERSONS_WITH_DISABILITY = MainTags(id=409, key='Persons with Disability', version=SPECIFIC_NEEDS_GROUP_VERSION)
    PREGNANT_OR_LACTATING_WOMEN = MainTags(id=410, key='Pregnant or Lactating Women', version=SPECIFIC_NEEDS_GROUP_VERSION)
    SINGLE_WOMEN_INCLUDING_WIDOWS = MainTags(id=411, key='Single Women (including Widows)', version=SPECIFIC_NEEDS_GROUP_VERSION)
    UNACCOMPANIED_OR_SEPARATED_CHILDREN = MainTags(id=412, key='Unaccompanied or Separated Children', version=SPECIFIC_NEEDS_GROUP_VERSION)

    # Gender
    FEMALE = MainTags(id=501, key='Female', version=GENDER_VERSION)
    MALE = MainTags(id=502, key='Male', version=GENDER_VERSION)

    # Age
    ADULT_18_TO_59_YEARS_OLD = MainTags(id=701, key='Adult (18 to 59 years old)', version=AGE_VERSION)
    CHILDREN_YOUTH_5_TO_17 = MainTags(id=702, key='Children/Youth (5 to 17 years old)', version=AGE_VERSION)
    INFANTS_TODDLERS_LESS_THAN_5_YEARS = MainTags(id=703, key='Infants/Toddlers (<5 years old)', version=AGE_VERSION)
    OLDER_PERSION_60_PLUS = MainTags(id=704, key='Older Persons (60+ years old)', version=AGE_VERSION)

    # Severity
    CRITICAL = MainTags(id=601, key='Critical', version=SEVERITY_VERSION)
    MAJOR = MainTags(id=602, key='Major', version=SEVERITY_VERSION)
    MINOR_PROBLEM = MainTags(id=603, key='Minor Problem', version=SEVERITY_VERSION)
    NO_PROBLEM = MainTags(id=604, key='No problem', version=SEVERITY_VERSION)
    OF_CONCERN = MainTags(id=605, key='Of Concern', version=SEVERITY_VERSION)

    @classmethod
    def sector_list(cls):
        return [
            Tags.AGRICULTURE.value._asdict(),
            Tags.CROSS.value._asdict(),
            Tags.EDUCATION.value._asdict(),
            Tags.FOOD_SECURITY.value._asdict(),
            Tags.HEALTH.value._asdict(),
            Tags.LIVELIHOODS.value._asdict(),
            Tags.LOGISTICS.value._asdict(),
            Tags.NUTRITION.value._asdict(),
            Tags.PROTECTION.value._asdict(),
            Tags.SHELTER.value._asdict(),
            Tags.WASH.value._asdict()
        ]

    @classmethod
    def subpillars_1d_list(cls):
        return [
            Tags.CONTEXT_ENVIRONMENT.value._asdict(),
            Tags.CONTEXT_SOCIO_CULTURAL.value._asdict(),
            Tags.CONTEXT_ECONOMY.value._asdict(),
            Tags.CONTEXT_DEMOGRAPHY.value._asdict(),
            Tags.CONTEXT_LEGAL_AND_POLICY.value._asdict(),
            Tags.CONTEXT_SECURITY_AND_STABILITY.value._asdict(),
            Tags.CONTEXT_POLITICS.value._asdict(),
            Tags.SHOCK_EVENT_TYPE_AND_CHARACTERISTICS.value._asdict(),
            Tags.SHOCK_EVENT_UNDERLYING_AGGRAVATING_FACTORS.value._asdict(),
            Tags.SHOCK_EVENT_HAZARD_THREATS.value._asdict(),
            Tags.DISPLACEMENT_TYPE_NUMBERS_MOVEMENTS.value._asdict(),
            Tags.DISPLACEMENT_PUSH_FACTORS.value._asdict(),
            Tags.DISPLACEMENT_PULL_FACTORS.value._asdict(),
            Tags.DISPLACEMENT_INTENTIONS.value._asdict(),
            Tags.DISPLACEMENT_LOCAL_INTEGRATION.value._asdict(),
            Tags.CASUALTIES_INJURED.value._asdict(),
            Tags.CASUALTIES_MISSING.value._asdict(),
            Tags.CASUALTIES_DEAD.value._asdict(),
            Tags.HUMANITARIAN_ACCESS_RELIEF_TO_POPULATION.value._asdict(),
            Tags.HUMANITARIAN_ACCESS_POPULATION_TO_RELIEF.value._asdict(),
            Tags.HUMANITARIAN_ACCESS_PHYSICAL_CONSTRAINTS.value._asdict(),
            Tags.HUMANITARIAN_ACCESS_GAPS.value._asdict(),
            Tags.INFORMATION_AND_COMMUNICATION_MEANS_AND_PREFERENCES.value._asdict(),
            Tags.INFORMATION_AND_COMMUNICATION_INFO_CHALLENGES_AND_BARRIERS.value._asdict(),
            Tags.INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_POP.value._asdict(),
            Tags.INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_HUM.value._asdict(),
            Tags.COVID_19_CASES.value._asdict(),
            Tags.COVID_19_CONTACT_CASES.value._asdict(),
            Tags.COVID_19_DEATHS.value._asdict(),
            Tags.COVID_19_HOSPITALIZATION_AND_CARE.value._asdict(),
            Tags.COVID_19_RESTRICTION_MEASURES.value._asdict(),
            Tags.COVID_19_TESTING.value._asdict(),
            Tags.COVID_19_VACCINATION.value._asdict()
        ]

    @classmethod
    def subpillars_2d_list(cls):
        return [
            Tags.AT_RISK_NUMBER_OF_PEOPLE.value._asdict(),
            Tags.AT_RISK_VULNERABILITIES.value._asdict(),
            Tags.CAPACITIES_RESPONSE_INTERNATIONAL.value._asdict(),
            Tags.CAPACITIES_RESPONSE_LOCAL.value._asdict(),
            Tags.CAPACITIES_RESPONSE_NATIONAL.value._asdict(),
            Tags.CAPACITIES_RESPONSE_NUM_PEOPLE_REACHED.value._asdict(),
            Tags.HUMANITARIAN_CONDITIONS_COPING_MECHANISMS.value._asdict(),
            Tags.HUMANITARIAN_CONDITIONS_LIVING_STANDARDS.value._asdict(),
            Tags.HUMANITARIAN_CONDITIONS_NUM_PEOPLE_IN_NEED.value._asdict(),
            Tags.HUMANITARIAN_CONDITIONS_PHY_MENTAL_WELL_BEING.value._asdict(),
            Tags.IMPACT_DRIVER_AGGRAVATING_FACTORS.value._asdict(),
            Tags.IMPACT_ON_PEOPLE.value._asdict(),
            Tags.IMPACT_ON_SYSTEMS_SRV_NET.value._asdict(),
            Tags.IMPACT_NUM_OF_PEOPLE_AFFECTED.value._asdict(),
            Tags.PRIORITY_INTERVENTIONS_HUMANITARIAN_STAFF.value._asdict(),
            Tags.PRIORITY_INTERVENTIONS_EXPRESSED_BY_POPULATION.value._asdict(),
            Tags.PRIORITY_NEEDS_EXPRESSED_BY_HUMANITARIAN_STAFF.value._asdict(),
            Tags.PRIORITY_NEEDS_EXPRESSED_BY_POPULATION.value._asdict()
        ]

    @classmethod
    def specific_needs_group_list(cls):
        return [
            Tags.CHILD_HEAD_OF_HOUSEHOLD.value._asdict(),
            Tags.CHRONICALLY_ILL.value._asdict(),
            Tags.ELDERLY_HEAD_OF_HOUSEHOLD.value._asdict(),
            Tags.FEMALE_HEAD_OF_HOUSEHOLD.value._asdict(),
            Tags.GBV_SURVIVORS.value._asdict(),
            Tags.INDIGENOUS_PEOPLE.value._asdict(),
            Tags.LGBTQI.value._asdict(),
            Tags.MINORITIES.value._asdict(),
            Tags.PERSONS_WITH_DISABILITY.value._asdict(),
            Tags.PREGNANT_OR_LACTATING_WOMEN.value._asdict(),
            Tags.SINGLE_WOMEN_INCLUDING_WIDOWS.value._asdict(),
            Tags.UNACCOMPANIED_OR_SEPARATED_CHILDREN.value._asdict()
        ]

    @classmethod
    def gender_list(cls):
        return [
            Tags.FEMALE.value._asdict(),
            Tags.MALE.value._asdict()
        ]

    @classmethod
    def age_list(cls):
        return [
            Tags.ADULT_18_TO_59_YEARS_OLD.value._asdict(),
            Tags.CHILDREN_YOUTH_5_TO_17.value._asdict(),
            Tags.INFANTS_TODDLERS_LESS_THAN_5_YEARS.value._asdict(),
            Tags.OLDER_PERSION_60_PLUS.value._asdict()
        ]

    @classmethod
    def severity_list(cls):
        return [
            Tags.CRITICAL.value._asdict(),
            Tags.MAJOR.value._asdict(),
            Tags.MINOR_PROBLEM.value._asdict(),
            Tags.NO_PROBLEM.value._asdict(),
            Tags.OF_CONCERN.value._asdict()
        ]


def get_all_mappings():
    all_tags = Categories.all_models() + Tags.sector_list() + Tags.subpillars_1d_list() + \
        Tags.subpillars_2d_list() + Tags.specific_needs_group_list() + Tags.gender_list() + \
        Tags.age_list() + Tags.severity_list()
    return {
        d['key']: (d['id'], d['version']) for d in all_tags
    }

