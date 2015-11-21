#include "AudioBankSwitch.h"
#include "ExternDefs.h"

AudioBankSwitch::AudioBankSwitch(uint8_t p0, uint8_t p1, uint8_t p2) :
  _p0(p0), _p1(p1), _p2(p2) { }

int8_t AudioBankSwitch::getSwitchPosition(bool & changed) {
	int8_t bank = -1;
  if (LOW == digitalRead(_p0)) {
			bank = 0;
	} else if (LOW == digitalRead(_p1)) {
      bank = 1;
  } else if (LOW == digitalRead(_p2)) {
     bank = 2;
  }
    
	if (-1 < bank && _bank != bank) {
	   _bank = bank;
     changed = true;
	}

	return _bank;
}

uint8_t AudioBankSwitch::getBank(bool & changed) {
  
    return getSwitchPosition(changed);
}

