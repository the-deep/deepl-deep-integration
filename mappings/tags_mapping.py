from collections import namedtuple

from enum import Enum

from .constants import (
    SECTOR_VERSION,
    SUBPILLAR_VERSION,
    SECONDARY_TAGS_VERSION,
    SUBPILLARS_1D_VERSION,
    SUBPILLARS_2D_VERSION,
    AGE_VERSION,
    GENDER_VERSION,
    SPECIFIC_NEEDS_GROUP_VERSION,
    SEVERITY_VERSION,
    AFFECTED_GRP_VERSION
)

MainCategories = namedtuple('MainCategories', ['id', 'key', 'version'])
MainTags = namedtuple('MainTags', ['id', 'key', 'version'])


class Categories(Enum):
    SECTORS = MainCategories(id=1, key='sectors', version=SECTOR_VERSION)
    SUBPILLARS = MainCategories(id=2, key='subpillars', version=SUBPILLAR_VERSION)
    SECONDARY_TAGS = MainCategories(id=3, key='secondary_tags', version=SECONDARY_TAGS_VERSION)

    @classmethod
    def all_models(cls):
        return [
            Categories.SECTORS.value._asdict(),
            Categories.SUBPILLARS.value._asdict(),
            Categories.SECONDARY_TAGS.value._asdict()
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
    CHILD_HEAD_OF_HOUSEHOLD = MainTags(id=401, key='specific_needs_groups->Child Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    CHRONICALLY_ILL = MainTags(id=402, key='specific_needs_groups->Chronically Ill', version=SPECIFIC_NEEDS_GROUP_VERSION)
    ELDERLY_HEAD_OF_HOUSEHOLD = MainTags(id=403, key='specific_needs_groups->Elderly Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    FEMALE_HEAD_OF_HOUSEHOLD = MainTags(id=404, key='specific_needs_groups->Female Head of Household', version=SPECIFIC_NEEDS_GROUP_VERSION)
    GBV_SURVIVORS = MainTags(id=405, key='specific_needs_groups->GBV survivors', version=SPECIFIC_NEEDS_GROUP_VERSION)
    INDIGENOUS_PEOPLE = MainTags(id=406, key='specific_needs_groups->Indigenous people', version=SPECIFIC_NEEDS_GROUP_VERSION)
    LGBTQI = MainTags(id=407, key='specific_needs_groups->LGBTQI+', version=SPECIFIC_NEEDS_GROUP_VERSION)
    MINORITIES = MainTags(id=408, key='specific_needs_groups->Minorities', version=SPECIFIC_NEEDS_GROUP_VERSION)
    PERSONS_WITH_DISABILITY = MainTags(id=409, key='specific_needs_groups->Persons with Disability', version=SPECIFIC_NEEDS_GROUP_VERSION)
    PREGNANT_OR_LACTATING_WOMEN = MainTags(id=410, key='specific_needs_groups->Pregnant or Lactating Women', version=SPECIFIC_NEEDS_GROUP_VERSION)
    SINGLE_WOMEN_INCLUDING_WIDOWS = MainTags(id=411, key='specific_needs_groups->Single Women (including Widows)', version=SPECIFIC_NEEDS_GROUP_VERSION)
    UNACCOMPANIED_OR_SEPARATED_CHILDREN = MainTags(id=412, key='specific_needs_groups->Unaccompanied or Separated Children', version=SPECIFIC_NEEDS_GROUP_VERSION)

    # Gender
    FEMALE = MainTags(id=501, key='gender_kw_pred->Female', version=GENDER_VERSION)
    MALE = MainTags(id=502, key='gender_kw_pred->Male', version=GENDER_VERSION)

    # Age
    ADULT_18_TO_59_YEARS_OLD = MainTags(id=701, key='age_kw_pred->Adult (18 to 59 years old)', version=AGE_VERSION)
    CHILDREN_YOUTH_5_TO_17 = MainTags(id=702, key='age_kw_pred->Children/Youth (5 to 17 years old)', version=AGE_VERSION)
    INFANTS_TODDLERS_LESS_THAN_5_YEARS = MainTags(id=703, key='age_kw_pred->Infants/Toddlers (<5 years old)', version=AGE_VERSION)
    OLDER_PERSION_60_PLUS = MainTags(id=704, key='age_kw_pred->Older Persons (60+ years old)', version=AGE_VERSION)

    # Severity
    CRITICAL = MainTags(id=601, key='severity->Critical', version=SEVERITY_VERSION)
    MAJOR = MainTags(id=602, key='severity->Major', version=SEVERITY_VERSION)
    MINOR_PROBLEM = MainTags(id=603, key='severity->Minor Problem', version=SEVERITY_VERSION)
    NO_PROBLEM = MainTags(id=604, key='severity->No problem', version=SEVERITY_VERSION)
    OF_CONCERN = MainTags(id=605, key='severity->Of Concern', version=SEVERITY_VERSION)

    # Affected Groups
    ASYLUM_SEEKERS = MainTags(id=801, key='affected_groups_level_3_kw->Asylum Seekers', version=AFFECTED_GRP_VERSION)
    HOST = MainTags(id=802, key='affected_groups_level_3_kw->Host', version=AFFECTED_GRP_VERSION)
    IDP = MainTags(id=803, key='affected_groups_level_3_kw->IDP', version=AFFECTED_GRP_VERSION)
    MIGRANTS = MainTags(id=804, key='affected_groups_level_3_kw->Migrants', version=AFFECTED_GRP_VERSION)
    REFUGEES = MainTags(id=805, key='affected_groups_level_3_kw->Refugees', version=AFFECTED_GRP_VERSION)
    RETURNEES = MainTags(id=806, key='affected_groups_level_3_kw->Returnees', version=AFFECTED_GRP_VERSION)

    @classmethod
    def sector_list(cls):
        return [t.value._asdict() for t in [
            Tags.AGRICULTURE,
            Tags.CROSS,
            Tags.EDUCATION,
            Tags.FOOD_SECURITY,
            Tags.HEALTH,
            Tags.LIVELIHOODS,
            Tags.LOGISTICS,
            Tags.NUTRITION,
            Tags.PROTECTION,
            Tags.SHELTER,
            Tags.WASH
        ]]

    @classmethod
    def subpillars_1d_list(cls):
        return [t.value._asdict() for t in [
            Tags.CONTEXT_ENVIRONMENT,
            Tags.CONTEXT_SOCIO_CULTURAL,
            Tags.CONTEXT_ECONOMY,
            Tags.CONTEXT_DEMOGRAPHY,
            Tags.CONTEXT_LEGAL_AND_POLICY,
            Tags.CONTEXT_SECURITY_AND_STABILITY,
            Tags.CONTEXT_POLITICS,
            Tags.SHOCK_EVENT_TYPE_AND_CHARACTERISTICS,
            Tags.SHOCK_EVENT_UNDERLYING_AGGRAVATING_FACTORS,
            Tags.SHOCK_EVENT_HAZARD_THREATS,
            Tags.DISPLACEMENT_TYPE_NUMBERS_MOVEMENTS,
            Tags.DISPLACEMENT_PUSH_FACTORS,
            Tags.DISPLACEMENT_PULL_FACTORS,
            Tags.DISPLACEMENT_INTENTIONS,
            Tags.DISPLACEMENT_LOCAL_INTEGRATION,
            Tags.CASUALTIES_INJURED,
            Tags.CASUALTIES_MISSING,
            Tags.CASUALTIES_DEAD,
            Tags.HUMANITARIAN_ACCESS_RELIEF_TO_POPULATION,
            Tags.HUMANITARIAN_ACCESS_POPULATION_TO_RELIEF,
            Tags.HUMANITARIAN_ACCESS_PHYSICAL_CONSTRAINTS,
            Tags.HUMANITARIAN_ACCESS_GAPS,
            Tags.INFORMATION_AND_COMMUNICATION_MEANS_AND_PREFERENCES,
            Tags.INFORMATION_AND_COMMUNICATION_INFO_CHALLENGES_AND_BARRIERS,
            Tags.INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_POP,
            Tags.INFORMATION_AND_COMMUNICATION_KNOWLEDGE_AND_INFO_GAPS_HUM,
            Tags.COVID_19_CASES,
            Tags.COVID_19_CONTACT_CASES,
            Tags.COVID_19_DEATHS,
            Tags.COVID_19_HOSPITALIZATION_AND_CARE,
            Tags.COVID_19_RESTRICTION_MEASURES,
            Tags.COVID_19_TESTING,
            Tags.COVID_19_VACCINATION
        ]]

    @classmethod
    def subpillars_2d_list(cls):
        return [t.value._asdict() for t in [
            Tags.AT_RISK_NUMBER_OF_PEOPLE,
            Tags.AT_RISK_VULNERABILITIES,
            Tags.CAPACITIES_RESPONSE_INTERNATIONAL,
            Tags.CAPACITIES_RESPONSE_LOCAL,
            Tags.CAPACITIES_RESPONSE_NATIONAL,
            Tags.CAPACITIES_RESPONSE_NUM_PEOPLE_REACHED,
            Tags.HUMANITARIAN_CONDITIONS_COPING_MECHANISMS,
            Tags.HUMANITARIAN_CONDITIONS_LIVING_STANDARDS,
            Tags.HUMANITARIAN_CONDITIONS_NUM_PEOPLE_IN_NEED,
            Tags.HUMANITARIAN_CONDITIONS_PHY_MENTAL_WELL_BEING,
            Tags.IMPACT_DRIVER_AGGRAVATING_FACTORS,
            Tags.IMPACT_ON_PEOPLE,
            Tags.IMPACT_ON_SYSTEMS_SRV_NET,
            Tags.IMPACT_NUM_OF_PEOPLE_AFFECTED,
            Tags.PRIORITY_INTERVENTIONS_HUMANITARIAN_STAFF,
            Tags.PRIORITY_INTERVENTIONS_EXPRESSED_BY_POPULATION,
            Tags.PRIORITY_NEEDS_EXPRESSED_BY_HUMANITARIAN_STAFF,
            Tags.PRIORITY_NEEDS_EXPRESSED_BY_POPULATION
        ]]

    @classmethod
    def specific_needs_group_list(cls):
        return [t.value._asdict() for t in [
            Tags.CHILD_HEAD_OF_HOUSEHOLD,
            Tags.CHRONICALLY_ILL,
            Tags.ELDERLY_HEAD_OF_HOUSEHOLD,
            Tags.FEMALE_HEAD_OF_HOUSEHOLD,
            Tags.GBV_SURVIVORS,
            Tags.INDIGENOUS_PEOPLE,
            Tags.LGBTQI,
            Tags.MINORITIES,
            Tags.PERSONS_WITH_DISABILITY,
            Tags.PREGNANT_OR_LACTATING_WOMEN,
            Tags.SINGLE_WOMEN_INCLUDING_WIDOWS,
            Tags.UNACCOMPANIED_OR_SEPARATED_CHILDREN
        ]]

    @classmethod
    def gender_list(cls):
        return [t.value._asdict() for t in [
            Tags.FEMALE,
            Tags.MALE
        ]]

    @classmethod
    def age_list(cls):
        return [t.value._asdict() for t in [
            Tags.ADULT_18_TO_59_YEARS_OLD,
            Tags.CHILDREN_YOUTH_5_TO_17,
            Tags.INFANTS_TODDLERS_LESS_THAN_5_YEARS,
            Tags.OLDER_PERSION_60_PLUS
        ]]

    @classmethod
    def severity_list(cls):
        return [t.value._asdict() for t in [
            Tags.CRITICAL,
            Tags.MAJOR,
            Tags.MINOR_PROBLEM,
            Tags.NO_PROBLEM,
            Tags.OF_CONCERN
        ]]

    @classmethod
    def affected_group_list(cls):
        return [t.value._asdict() for t in [
            Tags.ASYLUM_SEEKERS,
            Tags.HOST,
            Tags.IDP,
            Tags.MIGRANTS,
            Tags.REFUGEES,
            Tags.RETURNEES
        ]]


def get_all_mappings():
    all_tags = Categories.all_models() + Tags.sector_list() + Tags.subpillars_1d_list() + \
        Tags.subpillars_2d_list() + Tags.specific_needs_group_list() + Tags.gender_list() + \
        Tags.age_list() + Tags.severity_list() + Tags.affected_group_list()
    return {
        d['key']: (d['id'], d['version']) for d in all_tags
    }


def get_categories():
    all_categories = Categories.all_models()
    return {
        d['key']: (d['id'], d['version']) for d in all_categories
    }
