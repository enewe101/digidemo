from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from digidemo.models import Proposal


def proposal(request, proposal_name):
	this_proposal = Proposal.objects.get(name=proposal_name)

	return render(
		request, 'digidemo/proposal.html', {'proposal':this_proposal})


def test(request):
	return render(request, 'digidemo/test.html', {})

