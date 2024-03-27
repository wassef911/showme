import pytest
from showme.tkq import run_coutries_by_name, run_coutries_by_eco, run_coutries_by_income

countries = ["France", "Tunisia"]
economies = ["7. Least developed region", "6. Developing region"]
incomes = ["7. Least developed region", "6. Developing region"]


@pytest.mark.anyio
async def test_run_coutries_by_name():
    task = await run_coutries_by_name.kiq(countries)
    result = (await task.wait_result()).return_value
    assert len(result) == 2
    for url in result:
        assert "https://showmedemo.blob.core.windows.net/showme/" in url


@pytest.mark.anyio
async def test_run_coutries_by_eco():
    task = await run_coutries_by_eco.kiq(economies)
    result = (await task.wait_result()).return_value
    assert len(result) == 2
    for url in result:
        assert "https://showmedemo.blob.core.windows.net/showme/" in url


@pytest.mark.anyio
async def test_run_coutries_by_income():
    task = await run_coutries_by_income.kiq(incomes)
    result = (await task.wait_result()).return_value
    assert len(result) == 2
    for url in result:
        assert "https://showmedemo.blob.core.windows.net/showme/" in url
